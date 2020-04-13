import csv
import os

FILE = "out.csv"

class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()


def write_to_csv(info_for_write):
    #notice use OrderedDict for save order
    fields = ['url','studio_name']
    file = FILE
    with open(file,'a+',encoding='utf-8-sig',newline='') as f:
        csv_dict = [row for row in csv.DictReader(f)]
        w = csv.DictWriter(f,fieldnames=fields)
        if os.stat(file).st_size == 0:
            w.writeheader()
        w.writerow(info_for_write)