import React from 'react'

class ChangeLanguage extends React.Component {
  // constructor(props){
  //   super(props)
  //   debugger;
  // }
  render = () => {
    return (
      <form action="/i18n/setlang/" method="post" style="display: inline;">
        {/*{% csrf_token %}*/}
        {/*<div class="form-group" style="display: inline;">*/}
          {/*<select class="form-control btn btn-default" name="language" onchange="javascript:form.submit()">*/}
            {/*{% for lang in LANGUAGES %}*/}
            {/*/!*<option value="{{ lang.0 }}"{% ifequal LANGUAGE_CODE lang.0 %}*!/*/}
                    {/*/!*selected="selected"{% endifequal %}>{{lang.1}}</option>*!/*/}
            {/*/!*{% endfor %}*!/*/}
          {/*</select>*/}
        {/*</div>*/}
      </form>
    )
  }
}

export default ChangeLanguage