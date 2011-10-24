import web
import json
import os

from libopf_py import OPF

urls = (
    '/(.*)', 'Service'
)
app = web.application(urls, globals())

#render = web.template.render('static/')

#http://johnpaulett.com/2008/09/20/getting-restful-with-webpy/
#http://hacks.mozilla.org/2009/07/cross-site-xmlhttprequest-with-cors/
#http://stackoverflow.com/questions/3595515/xmlhttprequest-error-origin-null-is-not-allowed-by-access-control-allow-origin

class Service:
    def GET(self, name):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        if not name:
          return open('index.html').read()
        else:
          f = "static/"+os.path.basename(name)
          return open(f).read()

    def POST(self, name):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        
        data = web.data()
        points = json.loads(data)
        
        import numpy
        from scikits.learn import svm
        
        feat  = numpy.array([[x,y] for (x,y,_) in points], dtype=numpy.float64)
        label = numpy.array([c for _,_,c in points],       dtype=numpy.float64)
        
        fit_indices     = numpy.where(label >= 0)
        predict_indices = numpy.where(label < 0)
        
        clf = OPF()
        clf.fit(feat[fit_indices], label[fit_indices].astype(numpy.int32))
        predicted = clf.predict(feat[predict_indices])

        label[predict_indices] = predicted

        msg = [(a[0], a[1], b) for (a,b) in zip(feat, label)]

        return json.dumps(msg)

if __name__ == "__main__":
    app.run()
