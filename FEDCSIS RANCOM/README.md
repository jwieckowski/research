### FLOW OF THE STUDY

The RANking COMparison (RANCOM) method was compared with Analytical Hierarchy Process (AHP) method in the practical problem of housing location selection.

These subjective weighting techniques were used to determine criteria weights based on individual preferences.

Three experts with different objectives were engaged in the study.

To verify which method handles the experts judgments inaccuracies better, 8 thresholds representing the inaccuracy levels were identified (5%, 10%, 15%, 20%, 25%, 30%, 35%, 40%).

Then, 9 selected Multi-Criteria Decision Analysis (MCDA) methods were applied to assess the decision variants based on the determined criteria weights.

### VISUALIZATIONS

In the `/img` folder, all visualizations generated based on the results obtained from the study are presented.

The name standard for the presented visualizations are as follows:

- `METHOD`_weights_`N`.pdf - represents the weights distributions for the `METHOD` (ahp, rancom) and `N` (number of expert: 1, 2, 3)
- cr\_`METHOD`.pdf - represents the consistency ratio for the `METHOD` (ahp, rancom)
- expert\_`N`\_weights.pdf - represents the weights for `N` (1, 2, 3) expert defined based on the criteria relevance judgment
- `METHOD`-`MCDA`-E`N`.pdf - represents the rankings from the assessment with combination of `METHOD` (ahp, rancom), `MCDA` method (ARAS, EDAS, COPRAS, MABAC, MOORA, TOPSIS, PROMETHEE II, VIKOR) and number of expert `N` (1, 2, 3)
- `MCDA`-`PERCENT`-Expert`N`.pdf - shows the flow of the rankings obtained with the `MCDA` method (ARAS, EDAS, COPRAS, MABAC, MOORA, TOPSIS, PROMETHEE II, VIKOR), with `PERCENT` inaccuracy level (5%, 10%, 15%, 20%, 25%, 30%, 35%, 40%) and for expert `N` (1, 2, 3)
- `MCDA`-Expert`N`.pdf - shows the assessment for all inaccuracy levels for the `MCDA` method (ARAS, EDAS, COPRAS, MABAC, MOORA, TOPSIS, PROMETHEE II, VIKOR) and for expert `N` (1, 2, 3)
- rw_ahp_rancom_corr_Expert`N`.pdf - represents the correlation of rw coefficient fot the AHP and RANCOM methods for the Expert `N` (1, 2, 3)
- ws_ahp_rancom_corr_Expert`N`.pdf - represents the correlation of WS coefficient fot the AHP and RANCOM methods for the Expert `N` (1, 2, 3)
- rw\_`METHOD`\_ref-rank-corr_Expert`N`.pdf - shows the rw correlation of MCDA assessment with the reference ranking obtained using `METHOD` (ahp, rancom)
- ws\_`METHOD`\_ref-rank-corr_Expert`N`.pdf - shows the WS correlation of MCDA assessment with the reference ranking obtained using `METHOD` (ahp, rancom)
