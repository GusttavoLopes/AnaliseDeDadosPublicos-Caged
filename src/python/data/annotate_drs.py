import unicodedata

import pandas as pd


def _remove_accentuation(text: str) -> str:
    """
    Removes accentuation from a given string.
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass

    text = unicodedata.normalize('NFKD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")

    return str(text)


def annotate_caged(
    processed_caged_path: str,
    sp_drs_map_path: str,
    annotated_caged_path: str
) -> str:
    """
    Annotatate São Paulo state DRS in CAGED processed data.

    Args:
        - processed_caged_path: path to CAGED data, this data is at
        `data/processed/caged_2020_processed_tabela_81.csv`.
        - sp_drs_map_path: São Paulo state drs map path. This data is available
        at `data/processed/sp_drs_map.csv`

    Returns:
        - path to annotated caged base in CSV format.
    """

    
    caged_df = pd.read_csv(processed_caged_path)
    sp_drs_map_df = pd.read_csv(sp_drs_map_path)

    
    caged_df = caged_df[caged_df['UF'] == 'SP'].copy()
    caged_df['Município'] = \
        caged_df['Município'].str.upper()

    
    caged_df['Município'] = caged_df['Município'].apply(
        lambda x: x[3:]
    )

    
    caged_df['Município'] = caged_df['Município'].apply(
        lambda x: _remove_accentuation(x)
    )
    sp_drs_map_df['Município'] = sp_drs_map_df['Município'].apply(
        lambda x: _remove_accentuation(x)
    )

    annotated_caged_df = caged_df.merge(
        sp_drs_map_df, on='Município', how='left'
    )

    
    annotated_caged_df.to_csv(annotated_caged_path)

    return annotated_caged_path
