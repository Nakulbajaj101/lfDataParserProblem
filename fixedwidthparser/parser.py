#!/usr/bin/env python
# coding: utf-8
import csv
import errno
import json
import logging
import os
import random
import struct
import sys


def create_fake_data_config(spec_data={}, column_name_key="", prefix="foo"):
    """
    Function that takes in specs to generate data and all column names
    from the config data, and generates fake data config for each column
    and outputs a dictionary of the config
    """
    
    return {col:f"{prefix}{index+1}1,{prefix}{index+1}2,{prefix}{index+1}3".split(",") \
            for index, col in enumerate(spec_data[column_name_key])}

def create_fixed_length(value="",allowed_length=5):
    """
    Function to generate fixed length based on input and 
    maximum space allowed, if value exceeds maximum allowed,
    value is trimmed at the maximum point
    """
    
    if allowed_length < 1:
        return ""
    if len(value) <= allowed_length:
        return value.ljust(allowed_length)
    else:
        return value[0:allowed_length]

def create_fake_data(spec_data={}, column_name="",fake_data_config={}, offset_column=""):
    """
    Function to generate fake data based on column and column offsets specs,
    and utilising fake data config by randomly generating value from the config
    """
    
    return "".join(create_fixed_length(value=random.choice(fake_data_config[spec_data[column_name][index]]), 
                                      allowed_length=int(spec_data[offset_column][index]))\
                                                        for index in range(0, len(spec_data[column_name])))

def create_fixed_width_parser(field_widths=[]):
    """
    Function that takes in the column widths and maximum line width if available
    and based on creates a parser function to parse the fixed column text. If line width
    is not provided, it builds it utilises sum of all field widths
    """
    
    fmtstring = ''.join('{}{}'.format(abs(fw),'s')
                            for fw in field_widths)
    fieldstruct = struct.Struct(fmtstring)
    unpack = fieldstruct.unpack_from
    parser = lambda line: list(s.decode() for s in unpack(line.encode()))
    
    return parser

def generate_fixed_width_data(filepath="", spec_data={}, column_name_key="", offset_key="", 
                              encoding_key="", fake_data_config=None):
    """
    Function to generate fixed width data given input specs about column names
    and each column offset. Fake data will be appended if fake data config is provided
    """
    
    with open(file=filepath, 
              mode="w", 
              newline='', 
              encoding=spec_data[encoding_key]) as file:

        header="".join(create_fixed_length(value=col,allowed_length=int(offset))\
                      for col,offset in zip (spec_data[column_name_key], spec_data[offset_key]))
        
        file.write(header)
        if fake_data_config:
            #lets add ten more rows of fake data
            for row in range(0, 10):
                file.write(create_fake_data(spec_data=spec_data,
                                            column_name=column_name_key,
                                            fake_data_config=fake_data_config,
                                            offset_column=offset_key))
    pass

def parse_fixed_width_data(read_filepath="./read.csv", spec_data={}, read_encoding_key="", offset_key="", 
                          output_encoding_key="", include_header=False, delimiter="|",
                          write_file_path="./write.csv"):
    """
    Function to read fixed width csv data and outputs a standard csv based on configuration provided
    of columns and offset required for each column
    """
    
    if os.path.exists(read_filepath):
        with open(file=read_filepath, 
                  mode="r", 
                  encoding=spec_data[read_encoding_key]) as readfile:
            data = csv.reader(readfile)
            field_widths = tuple([int(offset) for offset in spec_data[offset_key]])
            line_width = sum(width for width in field_widths)
            fixed_line_parser = create_fixed_width_parser(field_widths=field_widths)

            with open(file=write_file_path,
                      mode="w", 
                      encoding=spec_data[output_encoding_key]) as writefile:
                writer = csv.writer(writefile, delimiter=delimiter)
                for row in data:
                    
                    #Creating sublists from entire string based on total length of all offsets
                    chunks = [row[0][char:char+line_width] for char in range(0, len(row[0]), line_width)]
                    if include_header:
                        writer.writerow(fixed_line_parser(chunks[0]))
                        for chunk in range(1, len(chunks)):
                            writer.writerow(fixed_line_parser(chunks[chunk]))
                    else:
                        for chunk in chunks:
                            writer.writerow(fixed_line_parser(chunks[chunk]))
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), read_filepath)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    spec_file_path="./spec.json"
    fixed_width_file_path="./fwfile.csv"
    parsed_file_path="./parsedfwfile.csv"
    
    if os.path.exists(spec_file_path):
        with open(spec_file_path,"r") as spec:
            spec_data = json.load(spec)
        
        logging.info("Creating fake data config")
        fake_data_config = create_fake_data_config(spec_data=spec_data,
                                                column_name_key="ColumnNames")
        

        logging.info(f"Generating fixed width fake data at location {fixed_width_file_path} ")
        generate_fixed_width_data(filepath=fixed_width_file_path,
                                spec_data=spec_data,
                                column_name_key="ColumnNames",
                                offset_key="Offsets",
                                encoding_key="FixedWidthEncoding",
                                fake_data_config=fake_data_config)
        
        include_header=False
        if spec_data["IncludeHeader"].lower() == "true":
            include_header=True


        logging.info(f"Prasing file and generating standard file at location {parsed_file_path}")
        parse_fixed_width_data(read_filepath=fixed_width_file_path,
                            spec_data=spec_data,
                            read_encoding_key="FixedWidthEncoding",
                            output_encoding_key="DelimitedEncoding",
                            offset_key="Offsets",
                            include_header=include_header,
                            write_file_path=parsed_file_path
                            )
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), spec_file_path)
