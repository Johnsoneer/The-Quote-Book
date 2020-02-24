
function areYouSure(username,verify_username) {
  var txt
    if (confirm("Are you sure? Verify user "+verify_username+"?")) {
      document.location.href='/verify_user/'+username+'/'+verify_username;
    } else {
    document.location.href='/admin/'+username;
  }
  document.location.href='/admin/'+username
  ;
}

toLower = function(x){
  return x.toLowerCase();
};

function confirmNewQuotedPerson() {
  var user_input = document.getElementsByTagName('input')
  var user_names = []
  for (index = 0; index < user_input.length; index++) {
    if (!user_input[index].value.includes('.') && user_input[index].value.length>0) {
      user_names.push(user_input[index].value)
    }
  }
  var people = document.getElementById("quoted_person_name_list")
  var txt = "";
  var i;
  for (i = 0; i < people.options.length; i++) {
    txt = txt + people.options[i].value + ",";
  }
  var people_list = txt.split(',')
  for (index = 0; index < user_names.length; index++) {
    var person_to_compare = user_names[index].toLowerCase();
    if (people_list.map(toLower).includes(person_to_compare)==false &&
        confirm("This person you're quoting looks new. Make sure you've only \
listed their first name (no spaces). If someone else has their name \
already, then add their last initial.\n\n Add '"+user_names[index]+ "' to the \
list of people quoted?")){
        document.getElementById('quote_form').submit();
        console.log('confirmed');
      }  else if (people_list.map(toLower).includes(person_to_compare)){
        console.log('Name Existing in Database');
        document.getElementById('quote_form').submit();
      } else {
        console.log('Failed Confirmation');
      }
  }

};
