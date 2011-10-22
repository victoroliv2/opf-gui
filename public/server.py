import web
import json
from mimerender import mimerender

render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message

urls = (
    '/(.*)', 'Service'
)
app = web.application(urls, globals())

#http://johnpaulett.com/2008/09/20/getting-restful-with-webpy/

class Service:
    @mimerender(
        default = 'html',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, name):
        #http://hacks.mozilla.org/2009/07/cross-site-xmlhttprequest-with-cors/
        #http://stackoverflow.com/questions/3595515/xmlhttprequest-error-origin-null-is-not-allowed-by-access-control-allow-origin
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        import random
        
        return {'message': 'Hello! %d !' % random.randint(0, 1000)}

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
        
        clf = svm.SVC()
        clf.fit(feat[fit_indices], label[fit_indices])
        predicted = clf.predict(feat[predict_indices])
        
        print label, predict_indices, predicted
        
        label[predict_indices] = predicted
        
        msg = [(a[0], a[1], b) for (a,b) in zip(feat, label)]
        return json.dumps(msg)

if __name__ == "__main__":
    app.run()
