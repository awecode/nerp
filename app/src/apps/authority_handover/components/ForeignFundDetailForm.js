import React from 'react'
import { Field, FieldArray } from 'redux-form'
import { renderField, renderReactSelectWrapper } from '../../../project/components/ReduxFormFieldComponents'

class ForeignFundForm extends React.Component {
  // constructor(props){
  //   super(props)
  //   debugger;
  // }

  type_options = [
    {value: 'grant', label: 'Grant'},
    {value: 'loan', label: 'Loan'}
  ]

  sub_type_options = [
    {value: 'cash', label: 'Cash'},
    {value: 'reimbursable', label: 'Reimbursable'},
    {value: 'direct payment', label: 'Direct Payment'},
    {value: 'commodity', label: 'Commodity'}
  ]

  render = () => {
    // debugger;
    return (
      <div>
        {this.props.meta.error && <span>{this.props.meta.error}</span>}
        <table className="table table-striped input-table table-bordered">
          <thead>
          <th>Type</th>
          <th>Sub Type</th>
          <th>Donor</th>
          <th>Amount</th>
          </thead>
          <tbody>
          {this.props.fields.map(
            (foreign_fund, index) =>
              <tr>
                <td>
                  <Field name={`${foreign_fund}.type`} component={renderReactSelectWrapper}
                         label="Type"
                         options={this.type_options}
                  />
                </td>
                <td>
                  <Field name={`${foreign_fund}.subtype`} component={renderReactSelectWrapper}
                         label="Sub Type"
                         options={this.sub_type_options}
                  />
                </td>
                <td>
                  <Field name={`${foreign_fund}.donor`} component={renderReactSelectWrapper}
                         label="Donor"
                  />
                </td>
                <td>
                  <Field name={`${foreign_fund}.amount`} component={renderField}
                         label="Amount"
                         type="number"
                  />
                </td>
                <td>
                  <button
                    type="button"
                    title="Remove Fund"
                    className="btn btn-danger"
                    onClick={() => this.props.fields.remove(index)}
                  >Remove
                  </button>
                </td>
              </tr>
          )}

          </tbody>
        </table>
        <button type="button" onClick={() => this.props.fields.push({})} className="btn btn-success">
          Add Foreign Fund
        </button>
      </div>
    )
  }
}

export const renderForeignFundForm = props => (<ForeignFundForm {...props}/>)