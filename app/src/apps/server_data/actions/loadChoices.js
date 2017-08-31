export  const loadChoices = (app_name, model_name, data, status) => {
  return {
    type: 'LOAD_CHOICES',
    app_name: app_name,
    model_name: model_name,
    data: data,
    status: status
  }
}

export  const startLoadingChoices = (app_name, model_name) => {
  return {
    type: 'LOAD_CHOICES',
    app_name: app_name,
    model_name: model_name,
    data: [],
    status:{
      is_loading: true,
      error: null
    }
  }
}

export  const updateLoadingChoicesError = (app_name, model_name, error) => {
  return {
    type: 'LOAD_CHOICES_ERROR',
    app_name: app_name,
    model_name: model_name,
    data: [],
    status:{
      is_loading: false,
      error: error
    }
  }
}