import argparse,json,struct
from pathlib import Path

parser=argparse.ArgumentParser();parser.add_argument('video',type=Path);parser.add_argument('--count',type=int,default=600);args=parser.parse_args()
def boxes(data):
 offset=0
 while offset+8<=len(data):
  size,kind=struct.unpack_from('>I4s',data,offset);header=8
  if size==1:size=struct.unpack_from('>Q',data,offset+8)[0];header=16
  if size==0:size=len(data)-offset
  assert size>=header and offset+size<=len(data),(kind,size)
  yield kind,data[offset+header:offset+size]
  offset+=size
 assert offset==len(data),offset
def child(data,kind):return next(payload for name,payload in boxes(data) if name==kind)
movie=child(args.video.read_bytes(),b'moov');tracks=[]
for name,track in boxes(movie):
 if name!=b'trak':continue
 media=child(track,b'mdia');handler=child(media,b'hdlr')[8:12]
 tracks.append(handler.decode())
 if handler!=b'vide':continue
 header=child(media,b'mdhd');version=header[0]
 timescale=struct.unpack_from('>I',header,20 if version else 12)[0]
 samples=child(child(media,b'minf'),b'stbl');timing=child(samples,b'stts')
 runs=[struct.unpack_from('>II',timing,i) for i in range(8,len(timing),8)]
 count=sum(n for n,delta in runs);seconds=sum(n*delta for n,delta in runs)/timescale
 assert count==args.count and all(timescale/delta==30 for n,delta in runs),(count,runs,timescale)
 description=child(samples,b'stsd');codec,entry=next(boxes(description[8:]));width,height=struct.unpack_from('>HH',entry,24)
 assert codec==b'avc1' and (width,height)==(1920,1080),(codec,width,height)
assert tracks==['vide'],tracks
report={'file':args.video.name,'codec':'H.264','width':width,'height':height,'fps':30,'frames':count,'duration_seconds':seconds,'audio':False,'bytes':args.video.stat().st_size}
args.video.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
