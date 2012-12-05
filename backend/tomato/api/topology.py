# -*- coding: utf-8 -*-
# ToMaTo (Topology management software) 
# Copyright (C) 2010 Dennis Schwerdel, University of Kaiserslautern
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

def _getTopology(id_):
    top = topology.get(id_)
    fault.check(top, "Topology with id #%d does not exist", id_)
    return top

def topology_create():
    """
    Creates an empty topology.
    
    Return value:
      The return value of this method is the info dict of the new topology as
      returned by :py:func:`topology_info`. This info dict also contains the
      topology id that is needed for further manipulation of that object.
    """
    return topology.create().info()

def topology_remove(id): #@ReservedAssignment
    """
    Removes and empty topology.
    
    Return value:
      The return value of this method is ``None``.
      
    Exceptions:
      The topology must not contain elements or connections, otherwise the call
      will fail.
    """
    top = _getTopology(id)
    top.remove()

def topology_modify(id, attrs): #@ReservedAssignment
    """
    Modifies a topology, configuring it with the given attributes.
   
    Currently the only supported attribute for topologies is ``name``.
   
    Additional to the attributes that are supported by the topology,
    all attributes beginning with an underscore (``_``) will be accepted.
    This can be used to store addition information needed by a frontend.
    
    Parameter *id*:
      The parameter *id* identifies the topology by giving its unique id.
     
    Parameter *attrs*:
      The attributes of the topology can be given as the parameter *attrs*. 
      This parameter must be a dict of attributes.
    
    Return value:
      The return value of this method is the info dict of the topology as 
      returned by :py:func:`topology_info`. This info dict will reflect all
      attribute changes.    
    """
    top = _getTopology(id)
    top.modify(attrs)
    return top.info()

def topology_action(id, action, params={}): #@ReservedAssignment
    """
    Performs an action on the whole topology (i.e. on all elements) in a smart
    way.
    
    The following actions are currently supported by topologies:
    
      ``prepare``
        This action will execute the action ``prepare`` on all elements in the 
        state ``created``.
      
      ``destroy``
        This action will first execute the action ``stop`` on all elements in 
        the state ``started`` and then the action ``destroy`` on all elements 
        in the state ``prepared``.
        Note that the states of the elements will be re-evaluated after the 
        first round of actions.

      ``start``
        This action will first execute the action ``prepare`` on all elements
        in the state ``created`` and then the action ``start`` on all elements
        in the state ``prepared``.
        Note that the states of the elements will be re-evaluated after the 
        first round of actions.
      
      ``stop``
        This action will execute the action ``stop`` on all elements in the 
        state ``started``.
        
    Parameter *id*:
      The parameter *id* identifies the topology by giving its unique id.

    Parameter *action*:
      The parameter *action* is the action to execute on the topology.
     
    Parameter *params*:
      The parameters for the action (if needed) can be given as the parameter
      *params*. This parameter must be a dict if given.
    
    Return value:
      The return value of this method is  **not the info dict of the 
      topology**. Instead this method returns the result of the action. Changes
      of the action to the topology can be checked using 
      :py:func:`~topology_info`.    
    """
    top = _getTopology(id)
    return top.action(action, params)

def topology_info(id, full=False): #@ReservedAssignment
    """
    Retrieves information about a topology.
    
    Parameter *id*:
      The parameter *id* identifies the topology by giving its unique id.

    Parameter *full*:
      If this parameter is ``True``, the fields ``elements`` and 
      ``connections`` will be a list holding all information of 
      :py:func:`~backend.tomato.api.elements.element_info`
      and :py:func:`~backend.tomato.api.connections.connection_info`
      for each component.
      Otherwise these fields will be lists holding only the ids of the
      respective objects.

    Return value:
      The return value of this method is a dict containing information
      about this topology:

    ``id``
      The unique id of the topology.
      
    ``elements``
      A list with all elements. Depending on the parameter *full* this list
      includes the full information of the elements as given by 
      :py:func:`~backend.tomato.api.element.element_info` or only the id of the
      element.

    ``connections``
      A list with all connections. Depending on the parameter *full* this list
      includes the full information of the connections as given by 
      :py:func:`~backend.tomato.api.connection.connection_info` or only the id
      of the connection.
      
    ``attrs``
      A dict of attributes of this topology. If this topology does not have
      attributes, this field is ``{}``.    

    ``usage``
      The latest usage record of the type ``5minutes``. See 
      :doc:`/docs/accountingdata` for the contents of the field.

    ``permissions``
      A dict with usernames as the keys and permission levels as values.
    """
    top = _getTopology(id)
    return top.info(full)

def topology_list(full=False): #@ReservedAssignment
    """
    Retrieves information about all topologies the user can access.

    Parameter *full*:
      See :py:func:`~topology_info` for this parameter.
     
    Return value:
      A list with information entries of all topologies. Each list entry
      contains exactly the same information as returned by 
      :py:func:`topology_info`. If no topologies exist, the list is empty. 
    """
    tops = topology.getAll()
    return [top.info(full) for top in filter(lambda t:t.hasRole("user"), tops)]

def topology_permission(id, user, role): #@ReservedAssignment
    """
    Grants/changes permissions for a user on a topology. See :doc:`permissions`
    for further information about available roles and their meanings.
    
    Parameter *id*:
      The parameter *id* identifies the topology by giving its unique id.

    Parameter *user*:
      The name of the user.

    Parameter *role*:
      The name of the role for this user. If the user already has a role,
      if will be changed.
    """
    top = _getTopology(id)
    user = _getAccount(user)
    top.setRole(user, role)
    
def topology_usage(id): #@ReservedAssignment
    """
    Retrieves aggregated usage statistics for a topology.
    
    Parameter *id*:
      The parameter *id* identifies the topology by giving its unique id.

    Return value:
      Usage statistics for the given topology according to 
      :doc:`/docs/accountingdata`.
    """
    top = _getTopology(id)
    return top.totalUsage.info()    
    
from account import _getAccount
from .. import fault, topology