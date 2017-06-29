import React from 'react';
import ReactDOM from 'react-dom';
import {
    SearchkitManager,
    SearchkitProvider,
    SearchBox,
    Hits,
} from 'searchkit';

const sk = new SearchkitManager('/es');

class MovieHits extends Hits {
  renderResult(result) {
    return (
      <div key={result._id}>
        <a target="_blank">
          <div>{result._source.title}</div>
        </a>
      </div>
    );
  }
}

function App() {
  return (
    <div className="search-site">
      <SearchkitProvider searchkit={sk}>
        <div>
          <div className="search-site__query">
            <SearchBox />
          </div>

          <div className="search-site__results">
            <MovieHits hitsPerPage={10} />
          </div>
        </div>
      </SearchkitProvider>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
