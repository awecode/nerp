import {store} from '../../../project/store'

let initial_state = []
// let initial_state = store.server_data
export const serverData = (state = initial_state, action) => {
  switch (action.type) {
    case 'RECEIVE_GET_REQUEST':
      return state.map(todo =>
        (todo.id === action.id)
          ? {...todo, completed: !todo.completed}
          : todo
      )
    default:
      return state
  }
}