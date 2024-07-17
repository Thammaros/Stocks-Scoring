def criteria_1(info_dict:dict) -> float: 
    score = 0.0
    if info_dict['pegRatio'] and 0<info_dict['pegRatio']<1:
        score += float(1-info_dict['pegRatio'])
    if info_dict['returnOnAssets'] and info_dict['returnOnAssets']>0:
        score += float(min(info_dict['returnOnAssets'],0.5))*2
    if info_dict['returnOnEquity'] and info_dict['returnOnEquity']>0:
        score += float(min(info_dict['returnOnEquity'],0.5))*2
    if info_dict['quickRatio'] and info_dict['quickRatio']>1:
        score += float(min(info_dict['quickRatio'],2))/2
    if info_dict['currentRatio'] and info_dict['currentRatio']>1:
        score += float(min(info_dict['currentRatio'],2))/2
    if info_dict['priceToBook'] and 0<info_dict['priceToBook']<1:
        score += float(1-info_dict['priceToBook'])
    if info_dict['debtToEquity'] and 0<info_dict['debtToEquity']<1:
        score += float(1-info_dict['debtToEquity'])
    if info_dict['earningsGrowth'] and info_dict['earningsGrowth']>0:
        score += float(min(info_dict['earningsGrowth'],0.5))*2
    if info_dict['revenueGrowth'] and info_dict['revenueGrowth']>0:
        score += float(min(info_dict['revenueGrowth'],0.5))*2
    if info_dict['profitMargins'] and info_dict['profitMargins']>0:
        score += float(min(info_dict['profitMargins'],0.5))*2
    if info_dict['operatingMargins'] and info_dict['operatingMargins']>0:
        score += float(min(info_dict['operatingMargins'],0.5))*2
    if info_dict['grossMargins'] and info_dict['grossMargins']>0:
        score += float(min(info_dict['grossMargins'],0.5))*2
    if info_dict['ebitdaMargins'] and info_dict['ebitdaMargins']>0:
        score += float(min(info_dict['ebitdaMargins'],0.5))*2
    if info_dict['enterpriseToRevenue'] and 15>info_dict['enterpriseToRevenue']>0:
        score += float(1-info_dict['enterpriseToRevenue']/15)
    if info_dict['enterpriseToEbitda'] and 15>info_dict['enterpriseToEbitda']>0:
        score += float(1-info_dict['enterpriseToEbitda']/15)
    if info_dict['forwardPE'] and 0<info_dict['forwardPE']<15:
        score += float(1-info_dict['forwardPE']/15)
    if info_dict['trailingPE'] and 0<info_dict['trailingPE']<15:
        score += float(1-info_dict['trailingPE']/15)
    if info_dict['forwardPE'] and info_dict['trailingPE'] and 0<info_dict['forwardPE']<info_dict['trailingPE']:
        score += float(min((info_dict['trailingPE']-info_dict['forwardPE'])/info_dict['forwardPE'], 0.2))*5
    if info_dict['forwardEps'] and info_dict['forwardEps']>0:
        score += float(min(info_dict['forwardEps'],2))/2
    if info_dict['trailingEps'] and info_dict['trailingEps']>0:
        score += float(min(info_dict['trailingEps'],2))/2
    if info_dict['trailingEps'] and info_dict['forwardEps'] and info_dict['forwardEps']>info_dict['trailingEps']>0:
        score += float(min((info_dict['forwardEps']-info_dict['trailingEps'])/info_dict['trailingEps'], 0.5))*2
    if info_dict['revenuePerShare'] and info_dict['revenuePerShare']>0:
        score += 1
    if info_dict['payoutRatio'] and info_dict['payoutRatio']>0:
        score += float(min(info_dict['payoutRatio'],0.5))*2
    if info_dict['dividendYield'] and info_dict['dividendYield']>0.03:
        score += float(min(info_dict['dividendYield'],0.1))*10
    return score #24

def criteria_2(info_dict:dict, market_dict:dict) -> float:
    score = 2.0
    if info_dict['pegRatio'] and market_dict['pegRatio']:
        if market_dict['pegRatio']<info_dict['pegRatio']<0:
            score += 1
        elif market_dict['pegRatio']<0<info_dict['pegRatio']:
            score += 1
        elif 0<info_dict['pegRatio']<market_dict['pegRatio']:
            score += 1
    if info_dict['returnOnAssets'] and market_dict['returnOnAssets']:
        if info_dict['returnOnAssets']>market_dict['returnOnAssets']:
            score += 1
    if info_dict['returnOnEquity'] and market_dict['returnOnEquity']:
        if info_dict['returnOnEquity']>market_dict['returnOnEquity']:
            score += 1
    if info_dict['quickRatio'] and market_dict['quickRatio']:
        if info_dict['quickRatio']>market_dict['quickRatio']:
            score += 1
    if info_dict['currentRatio'] and market_dict['currentRatio']:
        if info_dict['currentRatio']>market_dict['currentRatio']:
            score += 1
    if info_dict['priceToBook'] and market_dict['priceToBook']:
        if info_dict['priceToBook']<market_dict['priceToBook']:
            score += 1
    if info_dict['debtToEquity'] and market_dict['debtToEquity']:
        if info_dict['debtToEquity']<market_dict['debtToEquity']:
            score += 1
    if info_dict['earningsGrowth'] and market_dict['earningsGrowth']:
        if info_dict['earningsGrowth']>market_dict['earningsGrowth']:
            score += 1
    if info_dict['revenueGrowth'] and market_dict['revenueGrowth']:
        if info_dict['revenueGrowth']>market_dict['revenueGrowth']:
            score += 1
    if info_dict['profitMargins'] and market_dict['profitMargins']:
        if info_dict['profitMargins']>market_dict['profitMargins']:
            score += 1
    if info_dict['operatingMargins'] and market_dict['operatingMargins']:
        if info_dict['operatingMargins']>market_dict['operatingMargins']:
            score += 1
    if info_dict['grossMargins'] and market_dict['grossMargins']:
        if info_dict['grossMargins']>market_dict['grossMargins']:
            score += 1
    if info_dict['ebitdaMargins'] and market_dict['ebitdaMargins']:
        if info_dict['ebitdaMargins']>market_dict['ebitdaMargins']:
            score += 1

    if info_dict['enterpriseToRevenue'] and market_dict['enterpriseToRevenue']:
        if market_dict['enterpriseToRevenue']<info_dict['enterpriseToRevenue']<0:
            score += 1
        elif market_dict['enterpriseToRevenue']<0<info_dict['enterpriseToRevenue']:
            score += 1
        elif 0<info_dict['enterpriseToRevenue']<market_dict['enterpriseToRevenue']:
            score += 1

    if info_dict['enterpriseToEbitda'] and market_dict['enterpriseToEbitda']:
        if market_dict['enterpriseToEbitda']<info_dict['enterpriseToEbitda']<0:
            score += 1
        elif market_dict['enterpriseToEbitda']<0<info_dict['enterpriseToEbitda']:
            score += 1
        elif 0<info_dict['enterpriseToEbitda']<market_dict['enterpriseToEbitda']:
            score += 1
            
    if info_dict['forwardPE'] and market_dict['forwardPE']:
        if market_dict['forwardPE']<info_dict['forwardPE']<0:
            score += 1
        elif market_dict['forwardPE']<0<info_dict['forwardPE']:
            score += 1
        elif 0<info_dict['forwardPE']<market_dict['forwardPE']:
            score += 1
    if info_dict['trailingPE'] and market_dict['trailingPE']:
        if market_dict['trailingPE']<info_dict['trailingPE']<0:
            score += 1
        elif market_dict['trailingPE']<0<info_dict['trailingPE']:
            score += 1
        elif 0<info_dict['trailingPE']<market_dict['trailingPE']:
            score += 1
    # if info_dict['trailingPE'] and info_dict['forwardPE'] and market_dict['trailingPE'] and market_dict['forwardPE']:
    #     if (info_dict['trailingPE'] - info_dict['forwardPE'])>(market_dict['trailingPE'] - market_dict['forwardPE']):
    #         score += 1

    if info_dict['forwardEps'] and market_dict['forwardEps']:
        if info_dict['forwardEps']>market_dict['forwardEps']:
            score += 1
    if info_dict['trailingEps'] and market_dict['trailingEps']:
        if info_dict['trailingEps']>market_dict['trailingEps']:
            score += 1
    # if info_dict['trailingEps'] and info_dict['forwardEps'] and market_dict['trailingEps'] and market_dict['forwardEps']:
    #     if (info_dict['forwardEps'] - info_dict['trailingEps'])>(market_dict['forwardEps'] - market_dict['trailingEps']):
    #         score += 1
            
    if info_dict['revenuePerShare'] and market_dict['revenuePerShare']:
        if info_dict['revenuePerShare']>market_dict['revenuePerShare']:
            score += 1
    if info_dict['payoutRatio'] and market_dict['payoutRatio']:
        if info_dict['payoutRatio']>market_dict['payoutRatio']:
            score += 1
    if info_dict['dividendYield'] and market_dict['dividendYield']:
        if info_dict['dividendYield']>market_dict['dividendYield']:
            score += 1
    return score #24