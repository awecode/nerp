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
        <div className="col-12">
          <button type="button" onClick={() => this.props.fields.push({})} className="btn btn-success">
            Add Foreign Fund
          </button>
        </div>

        {this.props.meta.error && <span>{this.props.meta.error}</span>}
        {this.props.fields.map(
          (foreign_fund, index) =>
            <div className="card">
              <div className="card-block">
                <div className="row" key={index}>
                  <div className="col-sm-6 col-md-3">
                    <Field name={`${foreign_fund}.type`} component={renderReactSelectWrapper}
                           label="Type"
                           options={this.type_options}
                    />
                  </div>
                  <div className="col-sm-6 col-md-3">
                    <Field name={`${foreign_fund}.subtype`} component={renderReactSelectWrapper}
                           label="Sub Type"
                           options={this.sub_type_options}
                    />
                  </div>
                  <div className="col-sm-6 col-md-3">
                    <Field name={`${foreign_fund}.donor`} component={renderReactSelectWrapper}
                           label="Donor"
                    />
                  </div>

                  <div className="col-sm-6 col-md-3">
                    <Field name={`${foreign_fund}.amount`} component={renderField}
                           label="Amount"
                           type="number"
                    />

                  </div>
                  <div className="col-sm-6 col-md-3">
                    <button
                      type="button"
                      title="Remove Fund"
                      className="btn btn-danger"
                      onClick={() => this.props.fields.remove(index)}
                    >Remove Foreign Fund
                    </button>
                  </div>
                </div>
              </div>
            </div>
        )}
      </div>
    )
  }
}

export const renderForeignFundForm = props => (<ForeignFundForm {...props}/>)