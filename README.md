# Scoring Tools in Python (`scorpy`)

Tired of spending any amount of time scoring new surveys? Me too! So I created this package to help streamline this tedious task.

## Installation

```
pip install git+https://github.com/shawnrhoads/scorpy
```

## Usage

This package contains three main functions:
- `create_key(key_dict, scale)`: creates (or overwrites) `keys/*key.csv` and `keys/*key.json` files for any survey according to the specified settings in the dictionary key
- `score_surveys(data_file, scale_list)`: reads csv file (`data_file`) and scores a list of surveys to score (`scale_list`), outputs a new dataframe with scored surveys and respective subscales
- `reverse(this_val, min_val, max_val)`: reverse scores items in `data` prior to scoring if needed

**Example:**
```{python}
from scorpy import score_surveys

data_file  = "data.csv"           # data to score
scale_list = ["hexaco", "tripm"]  # key names that are available
method     = "average"            # method to score any subscale ("average" or "sum")

scored_data = score_surveys(data_file, scale_list, method)
```

### Current Surveys
| Scale          | Number of Items       | Reference                 | Code      |
|----------------|-----------------------|---------------------------|-----------|
| DOSPERT        | 60 items              | Blais et al., 2006        | `dospert` |
| HEXACO-PI-R    | 60 items + 4 Altruism | Ashton & Lee, 2008        | `hexaco`  |
| IRQ            | 16 items              | Williams et al., 2018     | `irq`     |
| IRI            | 28 items              | Davis, 1980               | `iri`     |
| ISEL           | 40 items              | Cohen & Hoberman, 1983    | `isel`    |
| PPI-Short      | 56 items              | Lilienfeld & Widows, 2005 | `ppi`     |
| QCAE           | 31 items              | Reniers et al., 2011      | `qcae`    |
| SRQ            | 23 items              | Foulkes et al., 2014      | `srq`     |
| STAI-Y2 Traits | 20 items              | Spielberger et al., 1983  | `stai`    |
| TriPM          | 58 items              | Patrick et al., 2009      | `tripm`   |


## Contributing

### Report bugs 

You can also contribute by adding any improvement to this package and reporting any issues/bugs so that they can be addressed.

### Add new keys

You can contribute to this package by adding a new key (`*key.csv` + `*key.json`). If you do so, please submit a pull request adding the new `.csv` and `.json` files with the heuristic `keys/["ScaleName"]_key` and a new entry in the "Current Surveys" and "Contributors" tables in the `README.md` file. In the pull request, you should also include (1) the dictionary you input into `create_key()` to generate the new key file and (2) a reference (i.e., APA citation and/or web link) from which you acquired the scoring key.

**Example template to use for generating a new key**
```{python}
from scorpy import create_key

scale_name = ''
subscales = {}
subscales['']  = []
subscales['']  = []
subscales['']  = [] # add more entries if needed
reversed_items = []

max_val = ...
min_val = ...

for key, vals in subscales.items():
    for idx, i in enumerate(vals):
        if i in reversed_items:
            subscales[key][idx] = str(i)+'R'
        else:
            subscales[key][idx] = str(i)

test = create_key(subscales, scale_name, min_val, max_val)
```

## Contributors

<table role="table" style="margin: 0px auto;">
    <thead role="rowgroup">
        <tr role="row">
            <td align="center" role="columnheader"><a target="_blank" rel="noopener noreferrer" href="https://shawnrhoads.github.io/"><img src="https://avatars3.githubusercontent.com/u/24925845" width="100px;" alt=""/></a><br /><sub><a target="_blank" rel="noopener noreferrer" href="https://github.com/shawnrhoads/gu-psyc-347/commits?author=shawnrhoads"><b>Shawn A Rhoads</b></a><br/><b title="Documentation">📖</b> <b title="Content">🖋</b> <b title="Code">💻</b><br><b title="Ideas">🤔</b> <b title="Maintenance">🚧</b> <b title="Reviewer">👀</b> </sub></td>
        </tr>
        </thead>
</table>

The above follows the <a target="blank" rel="noopener noreferrer" href="https://github.com/all-contributors/all-contributors">all-contributors</a> specification (see <a target="_blank" rel="noopener noreferrer" href="https://allcontributors.org/docs/en/emoji-key">emoji key</a>).