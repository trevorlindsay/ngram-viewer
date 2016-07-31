from flask import Flask, request, redirect, url_for
from flask import render_template

from search import search as searchBooks
from build_graph import build_graph, new_iplot


app = Flask(__name__)
graph = None

@app.route('/search', methods=['POST'])
def search():

    global graph

    ngrams = request.form['ngrams']
    data = searchBooks(ngrams)

    if not data:
        return redirect(url_for('main'))

    graph = new_iplot(build_graph(data))
    return redirect(url_for('show_results'))


@app.route('/')
@app.route('/index')
def main():
    return render_template('index.html')


@app.route('/results')
def show_results():

    global graph

    if not graph:
        return redirect(url_for('main'))

    with open('templates/results.html', 'wb') as f:
        with open('templates/resultstemplate.html') as r:
            html = r.read().replace('GraphPlaceholder', graph)
        f.write(html)

    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=False)




