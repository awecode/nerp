import { store } from '../../../project/store'
import update from 'immutability-helper'

// let initial_state = []
export const choiceReducer = ( state={} , action) => {
  switch (action.type) {
    case 'LOAD_CHOICES':
      let mod_state = {}
      if (state[action.app_name] === undefined) {
        let merge_obj = {}
        merge_obj[action.app_name] = {}
        merge_obj[action.app_name][action.model_name] = {}
        merge_obj[action.app_name][action.model_name]['status'] = action.status
        merge_obj[action.app_name][action.model_name]['data'] = action.data

        mod_state = update(state, {$merge: merge_obj})
        return mod_state
      }else if(state[action.app_name][action.model_name] === undefined){
        let merge_obj = {}
        merge_obj[action.model_name] = {}
        merge_obj[action.model_name]['status'] = action.status
        merge_obj[action.model_name]['data'] = action.data

        mod_state = update(state, {
          [action.app_name]: {$merge: merge_obj}
        })
        return mod_state
      }else{
        let merge_obj = {}
        merge_obj['status'] = action.status
        merge_obj['data'] = action.data

        mod_state = update(state, {
          [action.app_name]: {
            [action.model_name]: {$merge: merge_obj}
          }
        })
        return mod_state
      }
      return state

    default:
      return state
  }
}