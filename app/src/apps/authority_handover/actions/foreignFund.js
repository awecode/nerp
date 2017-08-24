export const addForeignFund = data => {
  return {
    type: 'ADD_FOREIGN_FUND',
    data: data
  }
}

export const removeForeignFund = (type, sub_type) => {
  return {
    type: 'REMOVE_FOREIGN_FUND',
    fType: type,
    fSubType: sub_type
  }
}