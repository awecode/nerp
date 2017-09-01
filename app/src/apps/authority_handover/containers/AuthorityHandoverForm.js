// Decorate with connect to read form values
import { formValueSelector } from 'redux-form'
import {connect} from 'react-redux'
import AuthorityHandover from '../components/AuthorityHandoverForm'
import { getOptions } from '../../server_data/actions/query'
const authorityHanoverSelector = formValueSelector('authority_handover') // <-- same as form name

const AuthorityHandoverForm = connect(state => {
    const beneficiary = authorityHanoverSelector(state, 'beneficiary')
    const parent = authorityHanoverSelector(state, 'parent')
    const fiscal_year = authorityHanoverSelector(state, 'fiscal_year')
    const budget_head = authorityHanoverSelector(state, 'budget_head')
    const priority = authorityHanoverSelector(state, 'priority')
  return {
    beneficiary,
    parent,
    fiscal_year,
    budget_head,
    priority,
    parent_options: getOptions(state, 'authority_handover', 'authority_handover', '/api/v1/authority-handover/choices/'),
    beneficiary_options: getOptions(state, 'authority_handover', 'beneficiary', '/api/v1/beneficiary/choices/'),
    fiscal_year_options: getOptions(state, 'core', 'fiscal_year', '/api/v1/fiscal-year/choices/'),
    budget_head_options: getOptions(state, 'core', 'budget_head', '/api/v1/budget-head/choices/'),
    expenditure_head_options: getOptions(state, 'authority_handover', 'expenditure_head', '/api/v1/expenditure-head/choices/'),
  }
})(AuthorityHandover)

export default AuthorityHandoverForm
