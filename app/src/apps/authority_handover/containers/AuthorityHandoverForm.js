// Decorate with connect to read form values
import { formValueSelector } from 'redux-form'
import {connect} from 'react-redux'
import AuthorityHandover from '../components/AuthorityHandoverForm'
const authorityHanoverSelector = formValueSelector('authority_handover') // <-- same as form name

const AuthorityHandoverForm = connect(state => {
  return {
    beneficiary: authorityHanoverSelector(state, 'beneficiary'),
    parent: authorityHanoverSelector(state, 'parent'),
    fiscal_year: authorityHanoverSelector(state, 'fiscal_year'),
    budget_head: authorityHanoverSelector(state, 'budget_head'),
  }
})(AuthorityHandover)

export default AuthorityHandoverForm
