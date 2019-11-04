.. highlight:: python

About Sphinx
============

Sphinx is a tool for making documentation. It was originally created for the
`Python documentation <https://docs.python.org/3/>`_, but is now used for many other software projects.

Sphinx uses :term:`reStructuredText` as its markup language.
It can produce HTML, LaTeX, ePub and PDF documents.

Source: https://www.sphinx-doc.org


Getting started
---------------

After installation, you can get started quickly with the tool 
:program:`sphinx-quickstart`. Just enter::

   sphinx-quickstart

Answer each question. Be sure to say *yes* to the **autodoc** extension.
This creates a directory with several documents:

- :file:`conf.py` file, the default configuration file
- :file:`index.rst` file, the master document

The :file:`conf.py` file let's you configure all aspects of Sphinx.
The :file:`index.rst` is the entry page for your documentation.

The ``toctree`` directive determines the files to include. 
For this project it looks like this::

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      1_intro/intro
      2_draw/draw
      3_image/image
      ...

To build the HTML pages just run::

   make html

To make the PDF document just run::

   make pdf

reStructuredText
----------------

reStructuredText (.rst) is the default markup language used with Sphinx.

- paragraphs are separated by one or more blank lines
- indentation is significant

Inline styles
^^^^^^^^^^^^^

- one asterisk for *italics*
- two asterisks for **bold**
- backquotes for ``code```

Lists
^^^^^

This code:

.. code-block:: none
   :linenos:

   * This is a bulleted list.
   * It has two items, the second
     item uses two lines.

   #. This is a numbered list.
   #. It has two items too.

produces this result:

* This is a bulleted list.
* It has two items, the second
  item uses two lines.

#. This is a numbered list.
#. It has two items too.

Hyperlinks
^^^^^^^^^^

This code::

   `Source <https://www.sphinx-doc.org>`_

produces `Source <https://www.sphinx-doc.org>`_

Admonitions
^^^^^^^^^^^

.. danger::
   Be careful with this code!

.. tip::
   Be careful with this code!

.. warning::
   Be careful with this code!

A directive consists of

- name
- arguments
- options
- content

Footnotes
^^^^^^^^^

This is a footnote [#f1]_ inside a text, tis is another one [#f2]_.

.. rubric:: Footnotes

.. [#f1] Text of the first footnote
.. [#f2] Text of the second footnote

Horizontal list
^^^^^^^^^^^^^^^

.. hlist::
   :columns: 3

   * happy
   * short
   * intelligent
   * thankful
   * displayed
   * horizontal

.. this is a comment

Download
^^^^^^^^

:download:`this example script <requirements.txt>`.

Include part of a file
----------------------

It is possible to include a Python object (class, method) from a file. 
For example you can include a **class** definition with::

   .. literalinclude:: 5_app/app.py
      :pyobject: Rectangle
      :linenos:
      :emphasize-lines: 5-7

resulting in

.. literalinclude:: 5_app/app.py
   :pyobject: Rectangle
   :linenos:
   :emphasize-lines: 5-7

Or you can include just a **method** definition with:: 

   .. literalinclude:: 5_app/app.py
      :pyobject: Rectangle.render

resulting in

.. literalinclude:: 5_app/app.py
   :pyobject: Rectangle.render

Domains
-------
Domains have been introduced into Sphinx to make it available for other languages than just Python.
Domains can provide custom indeces (like the Python module). 

.. function:: spam(eggs)
                 ham(eggs)

   Spam or ham the foo.

.. function:: filterwarnings(action, message)
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

Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

.. math:: e^{i\pi} + 1 = 0
   :label: euler

Euler's identity, equation :math:numref:`euler`, was elected one of the
most beautiful mathematical formulas.


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
