// todo get initial state somewhere
let initial_state = []
const foreignFunds = (state = initial_state, action) => {
  switch (action.type) {
    case 'ADD_FOREIGN_FUND':
      return [
        ...state,
        action.data
      ]
    case 'REMOVE_FOREIGN_FUND':
      return state.map(todo =>
        (todo.id === action.id)
          ? {...todo, completed: !todo.completed}
          : todo
      )
    default:
      return state
  }
}

export default todos