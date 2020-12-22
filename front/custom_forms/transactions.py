from ..forms import transactions
from datetime import datetime


def transactions_form(request, username, get_accounts, set_query):
    if request.method == 'POST':
        # OBTENER CUENTAS
        account_res = get_accounts(username)

        # CREAR FORMULARIO NUEVO
        form = transactions(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            amount = data.get('amount')
            description = data.get('description')
            originAccount = request.POST['originAccount']
            destAccount = request.POST['destAccount']
            now = datetime.now()
            date = now.strftime("%Y/%m/%d")

            # LEER ÚNICA CUENTA
            current_account = None
            for account in account_res:
                if str(account['id']) == str(originAccount):
                    current_account = account

            # VERIFICAR QUE NO SEA LA MISMA CUENTA
            if originAccount != destAccount:
                # VERIFICAR SI TIENE EL SALDO
                if float(current_account['balance']) >= float(amount):
                    # CREAR TRANSACCION
                    set_query(
                        f'INSERT INTO Transactions VALUES (null, {amount}, "{description}", "{date}", {originAccount}, {destAccount}, 0)')

                    # AGREGAR DEBITO A CUENTA
                    set_query(
                        f'UPDATE Account SET debit = debit + {float(amount)} WHERE id = {originAccount}')

                    # AGREGAR CREDITO A OTRA CUENTA
                    set_query(
                        f'UPDATE Account SET credit = credit + {float(amount)} WHERE id = {destAccount}')
