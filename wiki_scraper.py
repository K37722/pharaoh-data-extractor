#!/usr/bin/env python3
"""
Total War PHARAOH Wiki Scraper

Scrapes units, buildings, and factions data from Total War Wiki.
Exports to JSON and CSV formats.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import re
from pathlib import Path
from typing import List, Dict, Optional
import time
import argparse


class TotalWarWikiScraper:
    """Scraper for Total War PHARAOH Wiki data."""

    BASE_URL = "https://totalwar.fandom.com"

    def __init__(self, output_dir: str = "./wiki_data"):
        """Initialize the scraper."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TotalWarPharaohDataExtractor/1.0'
        })

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a wiki page."""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(1)  # Be nice to the server
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_units(self) -> List[Dict]:
        """Scrape unit data from the wiki."""
        print("\n" + "="*70)
        print("SCRAPING UNITS")
        print("="*70)

        units = []

        # Main units category page
        category_url = f"{self.BASE_URL}/wiki/Category:Units_(Total_War:_Pharaoh)"
        soup = self.fetch_page(category_url)

        if not soup:
            print("❌ Could not fetch units category page")
            return units

        # Find all unit links in the category
        unit_links = soup.find_all('a', {'class': 'category-page__member-link'})

        print(f"Found {len(unit_links)} unit pages")

        for i, link in enumerate(unit_links[:50], 1):  # Limit to first 50 for now
            unit_url = self.BASE_URL + link.get('href', '')
            unit_name = link.get('title', '')

            print(f"  [{i}/{min(len(unit_links), 50)}] {unit_name}")

            # Fetch individual unit page
            unit_soup = self.fetch_page(unit_url)
            if not unit_soup:
                continue

            unit_data = self.parse_unit_page(unit_soup, unit_name, unit_url)
            if unit_data:
                units.append(unit_data)

        print(f"\n✓ Scraped {len(units)} units")
        return units

    def parse_unit_page(self, soup: BeautifulSoup, name: str, url: str) -> Optional[Dict]:
        """Parse a single unit page."""
        unit = {
            'name': name,
            'url': url,
            'type': '',
            'faction': '',
            'stats': {},
            'abilities': [],
            'description': ''
        }

        # Look for infobox with stats
        infobox = soup.find('aside', {'class': 'portable-infobox'})
        if infobox:
            # Extract data from infobox rows
            for row in infobox.find_all('div', {'class': 'pi-item'}):
                label_elem = row.find('h3', {'class': 'pi-data-label'})
                value_elem = row.find('div', {'class': 'pi-data-value'})

                if label_elem and value_elem:
                    label = label_elem.get_text(strip=True)
                    value = value_elem.get_text(strip=True)

                    # Map common fields
                    if 'type' in label.lower() or 'class' in label.lower():
                        unit['type'] = value
                    elif 'faction' in label.lower():
                        unit['faction'] = value
                    else:
                        unit['stats'][label] = value

        # Extract description from content
        content = soup.find('div', {'id': 'mw-content-text'})
        if content:
            # Get first paragraph as description
            first_p = content.find('p')
            if first_p:
                unit['description'] = first_p.get_text(strip=True)[:500]

        return unit

    def scrape_buildings(self) -> List[Dict]:
        """Scrape building data from the wiki."""
        print("\n" + "="*70)
        print("SCRAPING BUILDINGS")
        print("="*70)

        buildings = []

        # Try to find buildings page
        buildings_url = f"{self.BASE_URL}/wiki/Buildings_(Total_War:_Pharaoh)"
        soup = self.fetch_page(buildings_url)

        if not soup:
            print("⚠️  Buildings page not found, trying alternative...")
            # Try category page
            buildings_url = f"{self.BASE_URL}/wiki/Category:Buildings_(Total_War:_Pharaoh)"
            soup = self.fetch_page(buildings_url)

        if soup:
            # Look for tables with building data
            tables = soup.find_all('table', {'class': 'wikitable'})

            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header

                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        building = {
                            'name': cells[0].get_text(strip=True),
                            'type': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                            'effects': [],
                            'cost': '',
                            'description': ''
                        }

                        # Try to extract more data
                        if len(cells) > 2:
                            building['effects'] = [cells[2].get_text(strip=True)]
                        if len(cells) > 3:
                            building['cost'] = cells[3].get_text(strip=True)

                        buildings.append(building)

        print(f"✓ Scraped {len(buildings)} buildings")
        return buildings

    def scrape_factions(self) -> List[Dict]:
        """Scrape faction data from the wiki."""
        print("\n" + "="*70)
        print("SCRAPING FACTIONS")
        print("="*70)

        factions = []

        # Factions page
        factions_url = f"{self.BASE_URL}/wiki/Factions_(Total_War:_Pharaoh)"
        soup = self.fetch_page(factions_url)

        if not soup:
            print("❌ Could not fetch factions page")
            return factions

        # Look for faction links and data
        content = soup.find('div', {'id': 'mw-content-text'})
        if content:
            # Find all links to faction pages
            faction_links = content.find_all('a', href=re.compile(r'/wiki/[^:]+\(Total_War:_Pharaoh\)'))

            seen_factions = set()

            for link in faction_links[:40]:  # Limit for now
                faction_name = link.get_text(strip=True)
                faction_url = self.BASE_URL + link.get('href', '')

                if not faction_name or faction_name in seen_factions:
                    continue

                seen_factions.add(faction_name)

                print(f"  Scraping: {faction_name}")

                # Fetch faction page
                faction_soup = self.fetch_page(faction_url)
                if faction_soup:
                    faction_data = self.parse_faction_page(faction_soup, faction_name, faction_url)
                    if faction_data:
                        factions.append(faction_data)

        print(f"✓ Scraped {len(factions)} factions")
        return factions

    def parse_faction_page(self, soup: BeautifulSoup, name: str, url: str) -> Optional[Dict]:
        """Parse a single faction page."""
        faction = {
            'name': name,
            'url': url,
            'culture': '',
            'leader': '',
            'bonuses': [],
            'units': [],
            'starting_region': '',
            'description': ''
        }

        # Look for infobox
        infobox = soup.find('aside', {'class': 'portable-infobox'})
        if infobox:
            for row in infobox.find_all('div', {'class': 'pi-item'}):
                label_elem = row.find('h3', {'class': 'pi-data-label'})
                value_elem = row.find('div', {'class': 'pi-data-value'})

                if label_elem and value_elem:
                    label = label_elem.get_text(strip=True).lower()
                    value = value_elem.get_text(strip=True)

                    if 'culture' in label:
                        faction['culture'] = value
                    elif 'leader' in label:
                        faction['leader'] = value
                    elif 'start' in label or 'region' in label:
                        faction['starting_region'] = value

        # Extract description
        content = soup.find('div', {'id': 'mw-content-text'})
        if content:
            first_p = content.find('p')
            if first_p:
                faction['description'] = first_p.get_text(strip=True)[:500]

        return faction

    def export_to_json(self, data: List[Dict], filename: str):
        """Export data to JSON file."""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Exported to: {output_path}")

    def export_to_csv(self, data: List[Dict], filename: str):
        """Export data to CSV file."""
        if not data:
            return

        output_path = self.output_dir / filename

        # Get all unique keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())

        fieldnames = sorted(all_keys)

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                # Convert lists/dicts to strings for CSV
                row = {}
                for key, value in item.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value)
                    else:
                        row[key] = value
                writer.writerow(row)

        print(f"💾 Exported to: {output_path}")

    def scrape_all(self):
        """Scrape all data types."""
        print("\n" + "="*70)
        print("TOTAL WAR PHARAOH WIKI SCRAPER")
        print("="*70)
        print("\n⚠️  This will scrape data from Total War Wiki")
        print("   Data completeness: ~70-80%")
        print("   May not include all hidden/unlisted content")
        print()

        # Scrape units
        units = self.scrape_units()
        if units:
            self.export_to_json(units, 'units.json')
            self.export_to_csv(units, 'units.csv')

        # Scrape buildings
        buildings = self.scrape_buildings()
        if buildings:
            self.export_to_json(buildings, 'buildings.json')
            self.export_to_csv(buildings, 'buildings.csv')

        # Scrape factions
        factions = self.scrape_factions()
        if factions:
            self.export_to_json(factions, 'factions.json')
            self.export_to_csv(factions, 'factions.csv')

        # Create summary
        summary = {
            'game': 'Total War PHARAOH DYNASTIES',
            'source': 'Total War Wiki (totalwar.fandom.com)',
            'scraped_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'units_count': len(units),
            'buildings_count': len(buildings),
            'factions_count': len(factions),
            'completeness': '~70-80% (wiki may not have all data)',
            'notes': 'Scraped from community wiki. Some data may be incomplete or outdated.'
        }

        self.export_to_json(summary, 'summary.json')

        print("\n" + "="*70)
        print("SCRAPING COMPLETE")
        print("="*70)
        print(f"\n📊 Results:")
        print(f"   Units: {len(units)}")
        print(f"   Buildings: {len(buildings)}")
        print(f"   Factions: {len(factions)}")
        print(f"\n📁 Output directory: {self.output_dir}/")
        print(f"\n💡 View your data:")
        print(f"   cat {self.output_dir}/units.json")
        print(f"   open {self.output_dir}/units.csv")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape Total War PHARAOH data from wiki"
    )

    parser.add_argument(
        'data_type',
        nargs='?',
        choices=['units', 'buildings', 'factions', 'all'],
        default='all',
        help='Type of data to scrape (default: all)'
    )

    parser.add_argument(
        '--output-dir',
        default='./wiki_data',
        help='Output directory (default: ./wiki_data)'
    )

    args = parser.parse_args()

    scraper = TotalWarWikiScraper(args.output_dir)

    if args.data_type == 'all':
        scraper.scrape_all()
    elif args.data_type == 'units':
        units = scraper.scrape_units()
        if units:
            scraper.export_to_json(units, 'units.json')
            scraper.export_to_csv(units, 'units.csv')
    elif args.data_type == 'buildings':
        buildings = scraper.scrape_buildings()
        if buildings:
            scraper.export_to_json(buildings, 'buildings.json')
            scraper.export_to_csv(buildings, 'buildings.csv')
    elif args.data_type == 'factions':
        factions = scraper.scrape_factions()
        if factions:
            scraper.export_to_json(factions, 'factions.json')
            scraper.export_to_csv(factions, 'factions.csv')


if __name__ == "__main__":
    main()
