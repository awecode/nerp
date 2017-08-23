import React from 'react'
import { Field, reduxForm } from 'redux-form'

class AuthorityHandoverForm extends React.Component {
  render () {
    return (
      <form onSubmit={handleSubmit}>
        {/* form body*/}
      </form>
    )
  }
}

AuthorityHandoverForm = reduxForm({
  // a unique name for the form
  form: 'authority_handover'
})(AuthorityHandoverForm)

// No need to connect()!
export default AuthorityHandoverForm