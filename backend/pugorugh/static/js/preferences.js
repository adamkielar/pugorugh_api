var Preferences = React.createClass({
  displayName: 'Preferences',

  data: {
    age: new Set(['b', 'y', 'a', 's']),
    gender: new Set(['m', 'f']),
    size: new Set(['s', 'm', 'l', 'xl']),
    pedigree: new Set(['y', 'n']),
    fur: new Set(['l', 's'])
  },
  getInitialState: function () {
    return { data: this.data };
  },
  componentDidMount: function () {
    this.serverRequest = $.ajax({
      url: "api/user/preferences/",
      method: "GET",
      dataType: "json",
      headers: TokenAuth.getAuthHeader()
    }).done(function (data) {
      this.data = {
        age: new Set(data.age ? data.age.split(",") : ['b', 'y', 'a', 's']),
        gender: new Set(data.gender ? data.gender.split(",") : ['m', 'f']),
        size: new Set(data.size ? data.size.split(",") : ['s', 'm', 'l', 'xl']),
        pedigree: new Set(data.pedigree ? data.pedigree.split(",") : ['y', 'n']),
        fur: new Set(data.fur ? data.fur.split(",") : ['l', 's'])
      };
      this.setState({ data: this.data });
    }.bind(this));
  },
  componentWillUnmount: function () {
    this.serverRequest.abort();
  },
  handleCheckboxGroupDataChanged: function (property, data) {
    this.data[property] = data;
  },
  save: function () {
    var json = JSON.stringify({
      age: Array.from(this.data.age).join(','),
      gender: Array.from(this.data.gender).join(','),
      size: Array.from(this.data.size).join(','),
      pedigree: Array.from(this.data.pedigree).join(','),
      fur: Array.from(this.data.fur).join(','),
    });

    $.ajax({
      url: "api/user/preferences/",
      method: "PUT",
      dataType: "json",
      headers: $.extend({ 'Content-type': 'application/json' }, TokenAuth.getAuthHeader()),
      data: json,
      success: this.props.setView.bind(this, 'undecided')
    });
  },
  render: function () {
    return React.createElement(
      'div',
      null,
      React.createElement(
        'h4',
        null,
        'Set Preferences'
      ),
      React.createElement(CheckboxGroup, {
        title: 'Gender',
        checkboxes: [{ label: "Male", value: "m" }, { label: "Female", value: "f" }],
        data: this.state.data.gender,
        onChange: this.handleCheckboxGroupDataChanged.bind(this, 'gender'),
        atLeastOne: true
      }),
      React.createElement(CheckboxGroup, {
        title: 'Age',
        checkboxes: [{ label: "Baby", value: "b" }, { label: "Young", value: "y" }, { label: "Adult", value: "a" }, { label: "Senior", value: "s" }],
        data: this.state.data.age,
        onChange: this.handleCheckboxGroupDataChanged.bind(this, 'age'),
        atLeastOne: true
      }),
      React.createElement(CheckboxGroup, {
        title: 'Size',
        checkboxes: [{ label: "Small", value: "s" }, { label: "Medium", value: "m" }, { label: "Large", value: "l" }, { label: "Extra Large", value: "xl" }],
        data: this.state.data.size,
        onChange: this.handleCheckboxGroupDataChanged.bind(this, 'size'),
        atLeastOne: true
      }),
      React.createElement(CheckboxGroup, {
        title: 'Pedigree',
        checkboxes: [{ label: "Yes", value: "y" }, { label: "No", value: "n" }],
        data: this.state.data.pedigree,
        onChange: this.handleCheckboxGroupDataChanged.bind(this, 'pedigree'),
        atLeastOne: true
      }),
      React.createElement(CheckboxGroup, {
        title: 'Fur',
        checkboxes: [{ label: "Long", value: "l" }, { label: "Short", value: "s" }],
        data: this.state.data.fur,
        onChange: this.handleCheckboxGroupDataChanged.bind(this, 'fur'),
        atLeastOne: true
      }),
      React.createElement('hr', null),
      React.createElement(
        'button',
        { className: 'button', onClick: this.save },
        'Save'
      )
    );
  }
});