import thunk from 'redux-thunk';
import logger from 'redux-logger';
import {routerReducer, syncHistoryWithStore} from 'react-router-redux';
import {createStore, combineReducers, applyMiddleware, compose} from 'redux';

// import {collegeListReducer, collegeDetailReducer} from './reducers/colleges';
// import {courseListReducer, courseDetailReducer} from './reducers/courses';
// import {universityListReducer, universityDetailReducer} from './reducers/universities';
// import {admissionListReducer, admissionDetailReducer} from './reducers/admissions';
// import {careerListReducer, careerDetailReducer} from './reducers/careers';
// import {eventListReducer, eventDetailReducer} from './reducers/events';
// import {newsListReducer, newsDetailReducer} from './reducers/news';
// import {scholarshipListReducer, scholarshipDetailReducer} from './reducers/scholarships';
// import {vacancyListReducer, vacancyDetailReducer} from './reducers/vacancies';
// import {rankListReducer, rankDetailReducer} from './reducers/ranks';
// import {pageListReducer, pageDetailReducer} from './reducers/pages';
// import {followListReducer} from './reducers/follows';
// import {facultyListReducer} from './reducers/faculty';
// import {fetchReducer} from './reducers/fetch';
// import {latestReducer} from './reducers/latest';
// import {advertisementReducer} from './reducers/advertisements';
// import {collegeCategoryListReducer} from './reducers/relatedFollow/college_categories';
// import {courseTypeListReducer} from './reducers/relatedFollow/course_types';
// import {districtListReducer} from './reducers/relatedFollow/districts';
// import {levelListReducer} from './reducers/relatedFollow/levels';
// import {facultyFollowListReducer} from './reducers/relatedFollow/faculties.js';
// import {universityCategoryListReducer} from './reducers/relatedFollow/university_categories';
// import {feedListReducer} from './reducers/feed';
// import {searchListReducer} from './reducers/search';
// import {openDB} from './indexedDB'
// import {councilListReducer, councilDetailReducer} from './reducers/councils';

const middleware = applyMiddleware(thunk, logger);
// const middleware = applyMiddleware(thunk);

let composeEnhancers;
if (typeof(window) !== 'undefined') {
  composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
} else {
  composeEnhancers = compose;
}


const appReducer = combineReducers({
  // colleges: combineReducers({
  //   college_list: collegeListReducer,
  //   college_detail: collegeDetailReducer
  // }),
  // councils: combineReducers({
  //   council_list: councilListReducer,
  //   council_detail: councilDetailReducer
  // }),
  // courses: combineReducers({
  //   course_list: courseListReducer,
  //   course_detail: courseDetailReducer
  // }),
  // universities: combineReducers({
  //   university_list: universityListReducer,
  //   university_detail: universityDetailReducer
  // }),
  // admissions: combineReducers({
  //   admission_list: admissionListReducer,
  //   admission_detail: admissionDetailReducer
  // }),
  // careers: combineReducers({
  //   career_list: careerListReducer,
  //   career_detail: careerDetailReducer
  // }),
  // events: combineReducers({
  //   event_list: eventListReducer,
  //   event_detail: eventDetailReducer
  // }),
  // news: combineReducers({
  //   news_list: newsListReducer,
  //   news_detail: newsDetailReducer
  // }),
  // scholarships: combineReducers({
  //   scholarship_list: scholarshipListReducer,
  //   scholarship_detail: scholarshipDetailReducer
  // }),
  // vacancies: combineReducers({
  //   vacancy_list: vacancyListReducer,
  //   vacancy_detail: vacancyDetailReducer
  // }),
  // ranks: combineReducers({
  //   rank_list: rankListReducer,
  //   rank_detail: rankDetailReducer
  // }),
  // pages: combineReducers({
  //   page_list: pageListReducer,
  //   page_detail: pageDetailReducer
  // }),
  // faculties: combineReducers({
  //   faculty_courses: facultyListReducer
  // }),
  // categories: combineReducers({
  //   college: combineReducers({
  //     college_categories: collegeCategoryListReducer,
  //     districts: districtListReducer,
  //     course_types: courseTypeListReducer
  //   }),
  //   course: combineReducers({
  //     faculties: facultyFollowListReducer,
  //     levels: levelListReducer
  //   }),
  //   university: combineReducers({
  //     university_categories: universityCategoryListReducer,
  //     faculties: facultyFollowListReducer
  //   })
  // }),
  // feed: feedListReducer,
  // search: searchListReducer,
  // latest: latestReducer,
  // fetch_state: fetchReducer,
  // followed_topic: followListReducer,
  // advertisements: advertisementReducer,
  routing: routerReducer
});

const rootReducer = (state, action) => {
  // if (action.type === 'SET_OFFLINE_STORE') {
  //   return action.payload;
  // }
  return appReducer(state, action);
};

let preloadedState = {};
if (typeof window !== 'undefined') {
  preloadedState = window.__PRELOADED_STATE__;

  delete window.__PRELOADED_STATE__;
}

export const store = createStore(
  rootReducer,
  preloadedState,
  composeEnhancers(middleware)
);

// const getInitialState = () => {
//   const idbKeyVal = openDB();
//   if (typeof(navigator) !== 'undefined') {
//     if (!navigator.onLine) {
//       idbKeyVal.get('state').then((data) => {
//         store.dispatch({type: 'SET_OFFLINE_STORE', payload: data})
//       });
//     }
//   }
// };
//
// getInitialState();


// store.subscribe(() => {
//   if (typeof(navigator) !== 'undefined') {
//     const idbKeyVal = openDB();
//     if (navigator.onLine) {
//       idbKeyVal.set('state', store.getState());
//     }
//   }
// });