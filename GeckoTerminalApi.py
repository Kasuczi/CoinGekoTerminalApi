import requests
import time
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GeckoTerminalAPI:
    BASE_URL = 'https://api.geckoterminal.com/api/v2'
    HEADERS = {'Accept': 'application/json;version=20230302'}
    RATE_LIMIT = 30
    DELAY = 60 / RATE_LIMIT

    def __init__(self):
        pass

    def get_networks(self):
        endpoint = '/networks'
        return self._make_request(endpoint)

    def get_new_pools(self, network, include=None):
        params = {'include': include}
        endpoint = f'/networks/{network}/new_pools'
        return self._make_paginated_request(endpoint, initial_params=params)

    def get_dexes(self, page=1, include=None):
        params = {'page': page, 'include': include}
        endpoint = f'/networks/{self.network}/dexes'
        return self._make_request(endpoint, params=params)

    def get_pools_by_address(self, address, include=None):
        params = {'include': include}
        endpoint = f'/networks/{self.network}/pools/{address}'
        return self._make_request(endpoint, params=params)

    def get_multiple_pools_by_addresses(self, addresses, page=1, include=None):
        params = {'page': page, 'include': include}
        endpoint = f'/networks/{self.network}/pools/multi/{addresses}'
        return self._make_request(endpoint, params=params)

    def get_trending_pools(self, page=1, include=None):
        params = {'page': page, 'include': include}
        endpoint = f'/networks/{self.network}/trending_pools'
        return self._make_request(endpoint, params=params)

    def get_global_trending_pools(self, page=1, include=None):
        params = {'page': page, 'include': include}
        endpoint = '/networks/trending_pools'
        return self._make_request(endpoint, params=params)

    def search_pools(self, query, page=1, include=None):
        params = {'query': query, 'network': self.network, 'page': page, 'include': include}
        endpoint = '/search/pools'
        return self._make_request(endpoint, params=params)

    def fetch_new_pools_continuously(self):
        while True:
            new_pools = self.get_new_pools()
            if new_pools:
                logging.info(new_pools)
            time.sleep(self.DELAY)

    def _make_request(self, endpoint, params=None):
        full_url = self.BASE_URL + endpoint
        try:
            logging.info(f"Making API request to {full_url}")
            response = requests.get(full_url, headers=self.HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif 'data' in data and isinstance(data['data'], list):
                df = pd.DataFrame(data['data'])
            elif 'results' in data and isinstance(data['results'], list):
                df = pd.DataFrame(data['results'])
            else:
                df = pd.json_normalize(data)  # Normalize semi-structured JSON data into a flat table

            if 'attributes' in df.columns:
                attributes_df = pd.json_normalize(df['attributes'])
                df = df.drop('attributes', axis=1).join(attributes_df)

            for nested_column in ['price_change_percentage', 'transactions', 'volume_usd']:
                if nested_column in df.columns:
                    nested_df = pd.json_normalize(df[nested_column])
                    nested_df.columns = [f"{nested_column}.{subcolumn}" for subcolumn in
                                         nested_df.columns]  # Prepend the parent column name
                    df = df.drop(nested_column, axis=1).join(nested_df)

            return df

        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logging.error("Oops: Something Else", err)

        return pd.DataFrame()  # Return an empty DataFrame if there was an exception

    def _make_paginated_request(self, endpoint, initial_params=None):
        page = 1
        all_data = []

        while True:
            params = {'page': page}
            if initial_params:
                params.update(initial_params)

            full_url = self.BASE_URL + endpoint
            try:
                logging.info(f"Making API request to {full_url}")
                response = requests.get(full_url, headers=self.HEADERS, params=params)
                response.raise_for_status()
                data = response.json()

                # Check if data is empty, indicating no more pages
                if not data.get('data') and not data.get('results'):
                    logging.info(f"No data found for page {page}")
                    break

                df = pd.json_normalize(data, 'data' if 'data' in data else 'results')
                all_data.append(df)

            except requests.exceptions.HTTPError as errh:
                logging.error(f"Http Error on page {page}: {errh}")
                break
            except requests.exceptions.ConnectionError as errc:
                logging.error(f"Error Connecting on page {page}: {errc}")
                break
            except requests.exceptions.Timeout as errt:
                logging.error(f"Timeout Error on page {page}: {errt}")
                break
            except requests.exceptions.RequestException as err:
                logging.error(f"Other Error on page {page}: {err}")
                break

            page += 1
            time.sleep(self.DELAY)

        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

