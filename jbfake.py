# -*- coding: utf-8 -*-
# ###########################################################################
# #
# #    Copyright (C) 2005-2019 manatlan manatlan[at]gmail(dot)com
# #
# # This program is free software; you can redistribute it and/or modify
# # it under the terms of the GNU General Public License as published
# # by the Free Software Foundation; version 2 only.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU General Public License for more details.
# #
# ###########################################################################

# this file is just a mock of jbapi.py
# just for own tests
def init(path):
    pass

def getTags():
    return [
        dict(
            name="people",
            children=[
                dict(
                    name="jules",
                    children=[]
                ),
                dict(
                    name="jim",
                    children=[]
                ),
            ]
        ),
        dict(
            name="animals",
            children=[]
        ),
    ]

def getFolders():
    return [
        dict(
            path="/root",
            items=0,
            expand=False,
            folders=[
                dict(
                    path="/root/first",
                    items=0,
                    expand=False,
                    folders=[
                    ],
                ),
                dict(
                    path="/root/second",
                    items=0,
                    expand=False,
                    folders=[
                    ],
                ),

            ],
        )
    ]

def selectFromFolder(path,all=False):
    return [
            dict(
                path="/dd/aaa/p001.jpg",                # full path (unique)
                tags=["yo","yi"],
                date="213213213213",
                comment="Rien de spe"
                resolution="42 x 42",
                rating=1,
            ),
            dict(
                path="/dd/bbb/p002.jpg",
                tags=["yo"],
                date="213213213213",
                comment=""
                resolution="42 x 42",
                rating=3,
            ),
            dict(
                path="/dd/aaa/p003.jpg",
                tags=["yo","yu"],
                date="213213213213",
                comment=""
                rating=2,
            ),
            dict(
                path="/dd/bbb/p004.jpg",
                tags=["yo"],
                date="213213213213",
                comment="que neni"
                rating=5,
            ),
        ]

def selectFromBasket():
    return selectFromFolder("","")

def selectFromTags(tags):
    return selectFromFolder("","")


def getThumb(path):
    import urllib.request
    return urllib.request.urlopen("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/220px-Cat03.jpg")

def getImage(path):
    return None
