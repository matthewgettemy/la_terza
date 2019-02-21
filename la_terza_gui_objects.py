# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class LaTerzaFrame
###########################################################################

class LaTerzaFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"La Terza Orders", pos = wx.DefaultPosition, size = wx.Size( 979,515 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.calendar = wx.adv.CalendarCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.CAL_SHOW_HOLIDAYS )
		bSizer4.Add( self.calendar, 0, wx.ALL, 5 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.order_control = wx.ListCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES )
		bSizer5.Add( self.order_control, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button21 = wx.Button( self.m_panel1, wx.ID_ANY, u"Get All Orders", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button21, 0, wx.ALL, 5 )

		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"Mark Order Complete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button2, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )


		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )


		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		bSizer2.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.calendar.Bind( wx.adv.EVT_CALENDAR, self.date_updated )
		self.m_button21.Bind( wx.EVT_BUTTON, self.update_order_table )
		self.m_button2.Bind( wx.EVT_BUTTON, self.mark_order_complete )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def date_updated( self, event ):
		event.Skip()

	def update_order_table( self, event ):
		event.Skip()

	def mark_order_complete( self, event ):
		event.Skip()


