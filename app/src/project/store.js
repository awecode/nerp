import thunk from 'redux-thunk';
import logger from 'redux-logger';
import {routerReducer, syncHistoryWithStore} from 'react-router-redux';
import {createStore, combineReducers, applyMiddleware, compose} from 'redux';
import { reducer as formReducer } from 'redux-form'

const middleware = applyMiddleware(thunk, logger);
// const middleware = applyMiddleware(thunk);

let composeEnhancers;
if (typeof(window) !== 'undefined') {
  composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
} else {
  composeEnhancers = compose;
}


const appReducer = combineReducers({
  routing: routerReducer,
  form: formReducer
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