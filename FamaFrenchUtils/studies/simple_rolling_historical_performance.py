import sys
import os

# Does not require try catch as this will work for anyone despite their setup but may not find the script.
sys.path.append(os.path.expanduser('~') + '/git/FamaFrenchUtils/')

import FamaFrenchUtils.data.industry_portfolios as ff_ip

data = ff_ip.industry_portfolio_csv()

rolling_3 = data.rolling(36)
rolling_5 = data.rolling(60)

roll_5_sharpe = (rolling_5.mean() / rolling_5.std()).dropna()  # For now, assuming FF is XR. TBD.

rank_roll_5 = roll_5_sharpe.rank(axis=1)
rank_roll_5.describe().T['mean'].sort_values()

rank_roll_5 = rolling_5.mean().rank(axis=1)
rank_roll_5.describe().T['mean'].sort_values()
