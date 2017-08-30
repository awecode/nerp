import fetch from 'isomorphic-fetch'

export const startGetRequest = (store_location) => {
  return {
    type: 'START_GET_REQUEST',
    store_location: store_location
  }
}

export const endGetRequest = (store_location) => {
  return {
    type: 'END_GET_REQUEST',
    store_location: store_location
  }
}

export const getRequestError = (store_location, error_data) => {
  return {
    type: 'GET_REQUEST_ERROR',
    store_location: store_location,
    error_data: error_data
  }
}

export const receiveGetRequest = (store_location, received_data) => {
  return {
    type: 'RECEIVE_GET_REQUEST',
    store_location: store_location,
    received_data: received_data,
    receivedAt: Date.now()
  }
}

function handleErrors(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}


export const fetchData = (url, store_location) => {
  return dispatch => {
    dispatch(startGetRequest(store_location))
    return fetch(url)
      .then(handleErrors)
      .then(response => response.json())
      .then(received_data =>
        dispatch(receiveGetRequest(store_location, received_data)),
        dispatch(endGetRequest(store_location))
      )
      // .catch(error => console.log(error) )
  }
}

