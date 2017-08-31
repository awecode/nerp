import fetch from 'isomorphic-fetch'
import { startLoadingChoices } from './loadChoices'


function handleErrors (response) {
  if (!response.ok) {
    throw Error(response.statusText)
  }
  return response
}

export const fetchData = (url, onStartCallbackAction, onLoadCallbackAction, actionArguments) => {
  return dispatch => {
    dispatch(onStartCallbackAction(...actionArguments))
    return fetch(url)
    // .then(handleErrors)
      .then(response => response.json())
      .then(received_data => {
          let args = [...actionArguments, received_data, {is_loading: false, error: null}]
          dispatch(onLoadCallbackAction(...args))
        }
      )
    // .catch(error => console.log(error) )
  }
}

