
function areYouSure(username,verify_username) {
  var txt
  console.log('Function is Firing.')
    if (confirm("Are you sure? Verify user "+verify_username+"?")) {
      document.location.href='/verify_user/'+username+'/'+verify_username;
    } else {
    document.location.href='/admin/'+username;
  }
  document.location.href='/admin/'+username
  ;
}
