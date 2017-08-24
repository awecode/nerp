import { combineReducers } from 'redux'


const todoApp = combineReducers({
  todos,
  visibilityFilter
})

export default todoApp