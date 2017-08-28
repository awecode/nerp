import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';

import {BrowserRouter as Router} from 'react-router-dom';
import AppRoute from './Route';
// import ScrollToTop from './ScrollToTop';
import {store} from './store';

import './bootstrap'

import './scss/project.scss'

// React devtool for preact
// import 'preact/devtools';

// if (data && action && !hydrate) {
//   switch (action) {
//     case 'LOAD_DATA_COLLEGE':
//       store.dispatch({'type': 'LOAD_DATA_COLLEGE', 'payload': data});
//       break;
//     case 'LOAD_DATA_COLLEGE_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_COLLEGE_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_COURSE':
//       store.dispatch({'type': 'LOAD_DATA_COURSE', 'payload': data});
//       break;
//     case 'LOAD_DATA_COURSE_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_COURSE_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_UNIVERSITY':
//       store.dispatch({'type': 'LOAD_DATA_UNIVERSITY', 'payload': data});
//       break;
//     case 'LOAD_DATA_UNIVERSITY_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_UNIVERSITY_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_ADMISSION':
//       store.dispatch({'type': 'LOAD_DATA_ADMISSION', 'payload': data});
//       break;
//     case 'LOAD_DATA_ADMISSION_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_ADMISSION_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_CAREER':
//       store.dispatch({'type': 'LOAD_DATA_CAREER', 'payload': data});
//       break;
//     case 'LOAD_DATA_CAREER_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_CAREER_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_EVENT':
//       store.dispatch({'type': 'LOAD_DATA_EVENT', 'payload': data});
//       break;
//     case 'LOAD_DATA_EVENT_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_EVENT_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_NEWS':
//       store.dispatch({'type': 'LOAD_DATA_NEWS', 'payload': data});
//       break;
//     case 'LOAD_DATA_NEWS_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_NEWS_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_SCHOLARSHIP':
//       store.dispatch({'type': 'LOAD_DATA_SCHOLARSHIP', 'payload': data});
//       break;
//     case 'LOAD_DATA_SCHOLARSHIP_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_SCHOLARSHIP_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_VACANCY':
//       store.dispatch({'type': 'LOAD_DATA_VACANCY', 'payload': data});
//       break;
//     case 'LOAD_DATA_VACANCY_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_VACANCY_DETAIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_FOLLOW':
//       store.dispatch({'type': 'LOAD_DATA_FOLLOW', 'payload': data});
//       break;
//     case 'LOAD_DATA_COUNCIL':
//       store.dispatch({'type': 'LOAD_DATA_COUNCIL', 'payload': data});
//       break;
//     case 'LOAD_DATA_COUNCIL_DETAIL':
//       store.dispatch({'type': 'LOAD_DATA_COUNCIL_DETAIL', 'payload': data});
//       break;
//     default:
//       break;
//   }
// }


ReactDOM.render(
  <Provider store={store}>
    <Router>
      <AppRoute />
    </Router>
  </Provider>,
  document.getElementById('app')
);