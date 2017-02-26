define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "C__Users_Aituglo_Dropbox_Onyx_Onyx_doc_main_js",
    "groupTitle": "C__Users_Aituglo_Dropbox_Onyx_Onyx_doc_main_js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/calendar",
    "title": "Add Event",
    "name": "addEvent",
    "group": "Calendar",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "title",
            "description": "<p>Title of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "notes",
            "description": "<p>Notes of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "lieu",
            "description": "<p>Place of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "datetime",
            "optional": false,
            "field": "start",
            "description": "<p>Start date of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "datetime",
            "optional": false,
            "field": "stop",
            "description": "<p>Stop date of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "color",
            "description": "<p>Color of Event</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Calendar</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This Event already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Calendar.py",
    "groupTitle": "Calendar"
  },
  {
    "type": "get",
    "url": "/calendar",
    "title": "Request Events Information",
    "name": "getEvent",
    "group": "Calendar",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "events",
            "description": "<p>List of Event</p>"
          },
          {
            "group": "200",
            "type": "Number",
            "optional": false,
            "field": "events.id",
            "description": "<p>Id of Event</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "events.title",
            "description": "<p>Title of Event</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "events.notes",
            "description": "<p>Notes of Event</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "events.lieu",
            "description": "<p>Place of Event</p>"
          },
          {
            "group": "200",
            "type": "datetime",
            "optional": false,
            "field": "events.start",
            "description": "<p>Start date of Event</p>"
          },
          {
            "group": "200",
            "type": "datetime",
            "optional": false,
            "field": "events.stop",
            "description": "<p>Stop date of Event</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "events.color",
            "description": "<p>Color of Event</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "EventNotFound",
            "description": "<p>No Event Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Calendar.py",
    "groupTitle": "Calendar"
  },
  {
    "type": "patch",
    "url": "/calendar",
    "title": "Update Date",
    "name": "updateEvent",
    "group": "Calendar",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "datetime",
            "optional": false,
            "field": "start",
            "description": "<p>Start date of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "datetime",
            "optional": false,
            "field": "stop",
            "description": "<p>Stop date of Event</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "json",
            "optional": false,
            "field": "status",
            "description": "<p>Status of Update</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "json",
            "optional": false,
            "field": "status",
            "description": "<p>An error has occurred</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Calendar.py",
    "groupTitle": "Calendar"
  },
  {
    "type": "put",
    "url": "/calendar/:id",
    "title": "Update Event",
    "name": "updateEvent",
    "group": "Calendar",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "boolean",
            "optional": false,
            "field": "delete",
            "description": "<p>Delete an Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "title",
            "description": "<p>Title of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "notes",
            "description": "<p>Notes of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "lieu",
            "description": "<p>Place of Event</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "color",
            "description": "<p>Color of Event</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Calendar</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This Event already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Calendar.py",
    "groupTitle": "Calendar"
  },
  {
    "type": "post",
    "url": "/house/add",
    "title": "Add House",
    "name": "addHouse",
    "group": "House",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of House</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "address",
            "description": "<p>Address of House</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "city",
            "description": "<p>City of House</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "country",
            "description": "<p>Country of House</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "latitude",
            "description": "<p>Latitude of House</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "longitude",
            "description": "<p>Longitude of House</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Option</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This House already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/House.py",
    "groupTitle": "House"
  },
  {
    "type": "delete",
    "url": "/house/delete",
    "title": "Delete House",
    "name": "deleteHouse",
    "group": "House",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>Id of House</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "delete",
            "description": "<p>House Deleted</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "HouseNotFound",
            "description": "<p>No House Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/House.py",
    "groupTitle": "House"
  },
  {
    "type": "get",
    "url": "/house",
    "title": "Request Houses Information",
    "name": "getHouse",
    "group": "House",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "houses",
            "description": "<p>List of House</p>"
          },
          {
            "group": "200",
            "type": "Number",
            "optional": false,
            "field": "houses.id",
            "description": "<p>Id of House</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "houses.name",
            "description": "<p>Name of House</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "houses.address",
            "description": "<p>Address of House</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "houses.city",
            "description": "<p>City of House</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "houses.country",
            "description": "<p>Country of House</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "houses.latitude",
            "description": "<p>Latitude of House</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "houses.longitude",
            "description": "<p>Longitude of House</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "HouseNotFound",
            "description": "<p>No House Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/House.py",
    "groupTitle": "House"
  },
  {
    "type": "post",
    "url": "/machine/add",
    "title": "Add Machine",
    "name": "addMachine",
    "group": "Machine",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "house",
            "description": "<p>House of Machine</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of Machine</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "room",
            "description": "<p>Room of Machine</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "host",
            "description": "<p>Host of Machine</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Option</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This Machine already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Machine.py",
    "groupTitle": "Machine"
  },
  {
    "type": "delete",
    "url": "/machine/delete",
    "title": "Delete Machine",
    "name": "deleteMachine",
    "group": "Machine",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>Id of Machine</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "delete",
            "description": "<p>Machine Deleted</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "MachineNotFound",
            "description": "<p>No Machine Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Machine.py",
    "groupTitle": "Machine"
  },
  {
    "type": "get",
    "url": "/machine",
    "title": "Request Machines Information",
    "name": "getMachine",
    "group": "Machine",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "machines",
            "description": "<p>List of Machines</p>"
          },
          {
            "group": "200",
            "type": "Number",
            "optional": false,
            "field": "machines.id",
            "description": "<p>Id of Machines</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "machines.house",
            "description": "<p>House of Machines</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "machines.name",
            "description": "<p>Name of Machines</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "machines.room",
            "description": "<p>Room of Machines</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "machines.host",
            "description": "<p>Host of Machines</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "MachineNotFound",
            "description": "<p>No Machine Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Machine.py",
    "groupTitle": "Machine"
  },
  {
    "type": "post",
    "url": "/room/add",
    "title": "Add Room",
    "name": "addRoom",
    "group": "Room",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "house",
            "description": "<p>House of Room</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of Room</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Option</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This Room already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Room.py",
    "groupTitle": "Room"
  },
  {
    "type": "delete",
    "url": "/room/delete",
    "title": "Delete Room",
    "name": "deleteRoom",
    "group": "Room",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>Id of Room</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "delete",
            "description": "<p>Room Deleted</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "RoomNotFound",
            "description": "<p>No Room Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Room.py",
    "groupTitle": "Room"
  },
  {
    "type": "get",
    "url": "/room",
    "title": "Request Rooms Information",
    "name": "getRoom",
    "group": "Room",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "rooms",
            "description": "<p>List of Rooms</p>"
          },
          {
            "group": "200",
            "type": "Number",
            "optional": false,
            "field": "rooms.id",
            "description": "<p>Id of Rooms</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "rooms.house",
            "description": "<p>House of Rooms</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "rooms.name",
            "description": "<p>Name of Rooms</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "RoomNotFound",
            "description": "<p>No Room Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Room.py",
    "groupTitle": "Room"
  },
  {
    "type": "get",
    "url": "/transport/metro/:string",
    "title": "Get Metro Info",
    "name": "getMetro",
    "group": "Transport___Metro",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of Metro</p>"
          },
          {
            "group": "200",
            "type": "select",
            "optional": false,
            "field": "station",
            "description": "<p>Get Station</p>"
          },
          {
            "group": "200",
            "type": "select",
            "optional": false,
            "field": "direction",
            "description": "<p>Get Direction</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "NoName",
            "description": "<p>No Metro Name Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/base/views/TransportController.py",
    "groupTitle": "Transport___Metro"
  },
  {
    "type": "post",
    "url": "/transport/metro/:string",
    "title": "Get Metro Schedule Info",
    "name": "serMetro",
    "group": "Transport___Metro",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of Metro</p>"
          },
          {
            "group": "Parameter",
            "type": "select",
            "optional": false,
            "field": "station",
            "description": "<p>Station</p>"
          },
          {
            "group": "Parameter",
            "type": "select",
            "optional": false,
            "field": "direction",
            "description": "<p>Direction</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Schedule Result</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "result.horaire",
            "description": "<p>Metro Schedule</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "result.name",
            "description": "<p>Metro Station</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "NoExist",
            "description": "<p>No Schedule Exist for This Station</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/base/views/TransportController.py",
    "groupTitle": "Transport___Metro"
  },
  {
    "type": "get",
    "url": "/transport/rer/:string",
    "title": "Get Rer Info",
    "name": "getRer",
    "group": "Transport___RER",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of RER</p>"
          },
          {
            "group": "200",
            "type": "select",
            "optional": false,
            "field": "station",
            "description": "<p>Get Station</p>"
          },
          {
            "group": "200",
            "type": "select",
            "optional": false,
            "field": "direction",
            "description": "<p>Get Direction</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "NoName",
            "description": "<p>No Rer Name Found</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/base/views/TransportController.py",
    "groupTitle": "Transport___RER"
  },
  {
    "type": "post",
    "url": "/transport/rer/:string",
    "title": "Get Rer Schedule Info",
    "name": "serRer",
    "group": "Transport___RER",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of RER</p>"
          },
          {
            "group": "Parameter",
            "type": "select",
            "optional": false,
            "field": "station",
            "description": "<p>Station</p>"
          },
          {
            "group": "Parameter",
            "type": "select",
            "optional": false,
            "field": "direction",
            "description": "<p>Direction</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Schedule Result</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "result.horaire",
            "description": "<p>Rer Schedule</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "result.name",
            "description": "<p>Rer Station</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "NoExist",
            "description": "<p>No Schedule Exist for This Rer</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/base/views/TransportController.py",
    "groupTitle": "Transport___RER"
  },
  {
    "type": "post",
    "url": "/user/change",
    "title": "Update Account",
    "name": "changeAccount",
    "group": "User",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>User Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>User Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>User Email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect To Change Account</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/delete/:id",
    "title": "Delete User",
    "name": "deleteAccount",
    "group": "User",
    "permission": [
      {
        "name": "authenticated"
      },
      {
        "name": "admin"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect To Manage Account</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/account/delete/:id",
    "title": "Update User",
    "name": "manageUser",
    "group": "User",
    "permission": [
      {
        "name": "authenticated"
      },
      {
        "name": "admin"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>User Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>User Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>User Email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect To Manage Account</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/manage/:id",
    "title": "Get User",
    "name": "manageUserGet",
    "group": "User",
    "permission": [
      {
        "name": "authenticated"
      },
      {
        "name": "admin"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "user",
            "description": "<p>Get User Information</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/user/login",
    "title": "Login User",
    "name": "registerUser",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>User Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>User Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "verifpassword",
            "description": "<p>User Verification Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>User Email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Hello</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This User already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/user",
    "title": "Register a User",
    "name": "registerUser",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>User Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>User Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "verifpassword",
            "description": "<p>User Verification Password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>User Email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "optional": false,
            "field": "redirect",
            "description": "<p>Redirect to Hello</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "AlreadyExist",
            "description": "<p>This User already Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/users",
    "title": "Get User",
    "name": "users",
    "group": "User",
    "permission": [
      {
        "name": "authenticated"
      },
      {
        "name": "admin"
      }
    ],
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "user",
            "description": "<p>Get All User Information</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/User.py",
    "groupTitle": "User"
  },
  {
    "type": "post",
    "url": "/wiki",
    "title": "Request Wiki Article",
    "name": "getArticle",
    "group": "Wiki",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "search",
            "description": "<p>Search Input</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "article",
            "description": "<p>List</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "article.head",
            "description": "<p>Header of Article</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "article.url",
            "description": "<p>Url of Article</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "article.summary",
            "description": "<p>Article Content</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "NoExist",
            "description": "<p>No Article Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/api/views/Wiki.py",
    "groupTitle": "Wiki"
  },
  {
    "type": "post",
    "url": "/wiki",
    "title": "Request Wiki Article",
    "name": "getArticle",
    "group": "Wiki",
    "permission": [
      {
        "name": "authenticated"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "search",
            "description": "<p>Search Input</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "200": [
          {
            "group": "200",
            "type": "Object[]",
            "optional": false,
            "field": "article",
            "description": "<p>List</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "article.head",
            "description": "<p>Header of Article</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "article.url",
            "description": "<p>Url of Article</p>"
          },
          {
            "group": "200",
            "type": "String",
            "optional": false,
            "field": "article.summary",
            "description": "<p>Article Content</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "NoExist",
            "description": "<p>No Article Exist</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./onyx/core/controllers/base/views/WikiController.py",
    "groupTitle": "Wiki"
  }
] });
