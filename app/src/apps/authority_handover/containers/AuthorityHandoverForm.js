// Decorate with connect to read form values
import { formValueSelector } from 'redux-form'
import {connect} from 'react-redux'
import AuthorityHandover from '../components/AuthorityHandoverForm'
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
    priority
  }
})(AuthorityHandover)

export default AuthorityHandoverForm
