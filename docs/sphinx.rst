About Sphinx
============

Sphinx is a tool for making documentation. It was originally created for the
Python documentation (https://docs.python.org/3/), but is now used for many other software projects.

Sphinx uses :term:`reStructuredText` as its markup language.

It can produce HTML, LaTeX, ePub and PDF documents.

Getting started
---------------

After installation, you can get started quickly with the tool 
:program:`sphinx-quickstart`. Just enter:

.. code-block:: shell

   $ sphinx-quickstart

Answer each question. Be sure to say *yes* to the **autodoc** extension.
This creates a directory several documents:

- :file:`conf.py` file, the default configuration file
- :file:`index.rst` file, the master document

The :file:`conf.py` is where you can configure all aspects of Sphinx.
The :file:`index.rst` is the 

The ``toctree`` directive determines the content of the document. For this document it looks 
like this::

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      1_intro/intro
      2_draw/draw
      3_image/image
      4_text/text
      5_app/app
      6_gui/gui
      7_sound/sound
      tutorial4/board
      sphinx

To build the HTML pages just run::

   make html

To make the PDF document just run::

   make pdf



Domains
-------
Domains have been introduced into Sphinx to make it available for other languages than just Python.
Domains can provide custom indeces (like the Python module). 

.. py:function:: spam(eggs)
                 ham(eggs)

   Spam or ham the foo.

.. py:function:: filterwarnings(action, message)
   :noindex:

The function :py:func:`spam` does a similar thing.

The class :class:`App` is always used to subclass a game application.

.. function:: pyfunc()

   Describes a Python function.

Reference to :func:`pyfunc` inmidst of text.

Cross-referencing syntax
------------------------

:meth:`~Queue.Queue.get` 

.. :module:: pygamelib

Directives
----------

This code::

   .. function:: Timer.repeat(repeat=3, number=1000)

      Descripe the function.

products this result::

.. function:: Timer.repeat(repeat=3, number=1000)

   Descripe the function.

.. method:: Timer.repeat(repeat=3, number=1000)

   Describe a method.

.. data:: number=1000

   Describe data.

.. class:: App

   Describe class without parameters.

   .. method:: run()

   Describe the method.

.. class:: App(parameters)

   Describe class with parameters.

   .. attribute:: objects

   Global class attribute.


.. py:function:: send_message(sender, recipient, message_body, [priority=1])

   Send a message to a recipient

   :param str sender: The person sending the message
   :param str recipient: The recipient of the message
   :param str message_body: The body of the message
   :param priority: The priority of the message, can be a number 1-5
   :type priority: integer or None
   :return: the message id
   :rtype: int
   :raises ValueError: if the message_body exceeds 160 characters
   :raises TypeError: if the message_body is not a basestring

   :type priorities: list(int)
   :type priorities: list(int)
   :type priorities: list[int]
   :type mapping: dict(str, int)
   :type mapping: dict[str, int]
   :type point: tuple(float, float)
   :type point: tuple[float, float]

The math domain
---------------

.. math:: e^{i\pi} + 1 = 0
   :label: euler

Euler's identity, equation :math:numref:`euler`, was elected one of the
most beautiful mathematical formulas.

html_sidebars = {
   '**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
   'using/windows': ['windowssidebar.html', 'searchbox.html'],
   }

The pygamelib module
--------------------

Classes are listed in alphabetical order.

.. automodule:: pygamelib
   :members:
   :member-order: bysource

The App class
--------------

.. autoclass:: pygamelib.App
   :members:
   :member-order: bysource
