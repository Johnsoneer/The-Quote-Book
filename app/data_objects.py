
class VerificationTable:

    '''
    An HTML string generator for a table featuring the following columns:

    - Username: String
    - Email: String
    - Verified: Boolean
    - Verify: Button Group
        - This will only populate when the user has not been verified already.
        - The button group calls the /verify_user url passing in the
            current user and the user to be verified.

    Call "ItemTable(input_data,user_obj).table_string" to get a HTML string for
    rendering the table.
    '''
    def __init__(self,input_data,user):
        self.row_string = "<tr>{}</tr>"
        self.cell_string = "<th>{}</th>"
        self.button_string = '<th><a href="/verify_user/<username>/<verify_username>"\
        <input type="button" value={}</th>'
        self.columns_string= "<thead><th>Username</th><th>Email</th><th>Verified Status</th>\
        <th>Verify User</th></thead>"
        self.rows = ''' '''
        for row_raw in input_data:
            row = row_raw.__dict__
            username = self.cell_string.format(row["username"])
            email = self.cell_string.format(row['email'])
            is_verified = self.cell_string.format(row['is_verified'])
            if row['is_verified']==True:
                verify = self.cell_string.format(self.button_string.format({"verify_username":row['username']
                                                        ,"username":user.username}))
            else:
                verify = self.cell_string.format('--')

            new_row = self.row_string.format(username+email+is_verified+verify)
            self.rows += new_row

        self.body_string = "<body>{}</body>".format(self.rows)
        self.table_string = "<table>{}</table>".format(self.columns_string+self.body_string)
