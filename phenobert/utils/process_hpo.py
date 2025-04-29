#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process HPO OBO file to generate JSON representation")
    parser.add_argument('--obo', required=True, help='Path to the HPO OBO file')
    parser.add_argument('--output', required=True, help='Path to save the output JSON file')
    return parser.parse_args()

class HPO_class:
    def __init__(self):
        self.Id = ""
        self.Name = []
        self.Alt_id = []
        self.Def = []
        self.Comment = []
        self.Synonym = []
        self.Xref = []
        self.Is_a = []
        self.Son = {}
        self.Father = {}
        self.Child = {}
    
    def to_dict(self):
        return {
            "Id": self.Id,
            "Name": self.Name,
            "Alt_id": self.Alt_id,
            "Def": self.Def,
            "Comment": self.Comment,
            "Synonym": self.Synonym,
            "Xref": self.Xref,
            "Is_a": self.Is_a,
            "Son": self.Son,
            "Father": self.Father,
            "Child": self.Child
        }

def parse_obo_file(obo_file_path):
    """
    Parse HPO OBO file and generate HPO class objects
    """
    HPOs = {}
    try:
        with open(obo_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            obo_terms = content.split("[Term]")
            
            for term in obo_terms:
                if "id: HP:" not in term:
                    continue
                
                hpo = HPO_class()
                lines = term.strip().split("\n")
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith("id: "):
                        hpo.Id = line.split("id: ")[1]
                    elif line.startswith("name: "):
                        hpo.Name.append(line.split("name: ")[1])
                    elif line.startswith("alt_id: "):
                        hpo.Alt_id.append(line.split("alt_id: ")[1])
                    elif line.startswith("def: "):
                        if '"' in line:
                            hpo.Def.append(line.split('"')[1])
                    elif line.startswith("comment: "):
                        hpo.Comment.append(line.split("comment: ")[1])
                    elif line.startswith("synonym: "):
                        if '"' in line:
                            hpo.Synonym.append(line.split('"')[1])
                        else:
                            hpo.Synonym.append(line.split("synonym: ")[1])
                    elif line.startswith("xref: "):
                        hpo.Xref.append(line.split("xref: ")[1])
                    elif line.startswith("is_a: "):
                        # Only add HPO number
                        parent_id = line.split("is_a: ")[1].split(" !")[0].strip()
                        hpo.Is_a.append(parent_id)
                
                if hpo.Id:
                    HPOs[hpo.Id] = hpo
        
        return HPOs
    except Exception as e:
        print(f"Error parsing OBO file: {str(e)}")
        sys.exit(1)

def find_ancestors(HPOs, ori_id, id):
    """
    Find all ancestors of a given HPO term
    """
    for parent_id in HPOs[id].Is_a:
        HPOs[ori_id].Father[parent_id] = True
        if parent_id in HPOs:
            find_ancestors(HPOs, ori_id, parent_id)

def build_hpo_relationships(HPOs):
    """
    Build relationships between HPO terms (parent-child, ancestors)
    """
    # Find all ancestors
    for id in HPOs:
        find_ancestors(HPOs, id, id)
    
    # Build direct children relationships
    for id in HPOs:
        for parent_id in HPOs[id].Is_a:
            if parent_id in HPOs:
                HPOs[parent_id].Son[id] = True
    
    # Build all descendants relationships
    for id in HPOs:
        for ancestor_id in HPOs[id].Father:
            if ancestor_id in HPOs:
                HPOs[ancestor_id].Child[id] = True
    
    return HPOs

def save_to_json(HPOs, output_path):
    """
    Save HPO dictionary to JSON file
    """
    try:
        hpos_dict = {id: HPOs[id].to_dict() for id in HPOs}
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(hpos_dict, file, ensure_ascii=False)
        print(f"Successfully saved HPO data to {output_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")
        sys.exit(1)

def main():
    args = parse_arguments()
    print(f"Processing HPO OBO file: {args.obo}")
    
    # Parse OBO file
    HPOs = parse_obo_file(args.obo)
    print(f"Found {len(HPOs)} HPO terms")
    
    # Build relationships
    HPOs = build_hpo_relationships(HPOs)
    
    # Save to JSON file
    save_to_json(HPOs, args.output)

if __name__ == "__main__":
    main() 