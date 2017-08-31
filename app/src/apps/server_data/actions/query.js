import { fetchData } from './getListAndDetail'
import { store } from '../../../project/store'
import { loadChoices, startLoadingChoices } from './loadChoices'

export const getOptions = (state, app_name, model_name, url) => {
  if (state.server_data.choices[app_name] !== undefined && state.server_data.choices[app_name][model_name] !== undefined) {
    if(!state.server_data.choices[app_name][model_name]['status']['is_loading']){
      return state.server_data.choices[app_name][model_name]['data']
    }
  } else {
    store.dispatch(
      fetchData(url, startLoadingChoices, loadChoices, [app_name, model_name]
      )
    )

  }
}