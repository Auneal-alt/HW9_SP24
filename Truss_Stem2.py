import math
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


class Position():
    """
    I made this position for holding a position in 3D space (i.e., a point).  I've given it some ability to do
    vector arithmitic and vector algebra (i.e., a dot product).  I could have used a numpy array, but I wanted
    to create my own.  This class uses operator overloading as explained in the class.
    """

    def __init__(self, pos=None, x=None, y=None, z=None):
        """
        x, y, and z have the expected meanings
        :param pos: a tuple (x,y,z)
        :param x: float
        :param y: float
        :param z: float
        """
        # set default values
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        # unpack position from a tuple if given
        if pos is not None:
            self.x, self.y, self.z = pos
        # override the x,y,z defaults if they are given as arguments
        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.z = z if z is not None else self.z

    # region operator overloads $NEW$ 4/7/21
    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        return True

    # this is overloading the addition operator.  Allows me to add Position objects with simple math: c=a+b, where
    # a, b, and c are all position objects.
    def __add__(self, other):
        return Position((self.x + other.x, self.y + other.y, self.z + other.z))

    # this overloads the iterative add operator
    def __iadd__(self, other):
        if other in (float, int):
            self.x += other
            self.y += other
            self.z += other
            return self
        if type(other) == Position:
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self

    # this is overloading the subtraction operator.  Allows me to subtract Positions. (i.e., c=b-a)
    def __sub__(self, other):
        return Position((self.x - other.x, self.y - other.y, self.z - other.z))

    # this overloads the iterative subtraction operator
    def __isub__(self, other):
        if other in (float, int):
            self.x -= other
            self.y -= other
            self.z -= other
            return self
        if type(other) == Position:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            return self

    # this is overloading the multiply operator.  Allows me to multiply a scalar or do a dot product (i.e., b=s*a or c=b*a)
    def __mul__(self, other):
        if type(other) in (float, int):
            return Position((self.x * other, self.y * other, self.z * other))
        if type(other) is Position:
            return Position((self.x * other.x, self.y * other.y, self.z * other.z))

    # this is overloading the __rmul__ operator so that s*Pt works.
    def __rmul__(self, other):
        return self * other

    # this is overloading the *= operator.  Same as a = Position((a.x*other, a.y*other, a.z*other))
    def __imul__(self, other):
        if type(other) in (float, int):
            self.x *= other
            self.y *= other
            self.z *= other
            return self

    # this is overloading the division operator.  Allows me to divide by a scalar (i.e., b=a/s)
    def __truediv__(self, other):
        if type(other) in (float, int):
            return Position((self.x / other, self.y / other, self.z / other))

    # this is overloading the /= operator.  Same as a = Position((a.x/other, a.y/other, a.z/other))
    def __idiv__(self, other):
        if type(other) in (float, int):
            self.x /= other
            self.y /= other
            self.z /= other
            return self

    # endregion

    def set(self, strXYZ=None, tupXYZ=None):
        """
        Sets the position of the string or tuple
        :param strXYZ: string
        :param tupXYZ: tuple
        :return: nothing
        """
        # set position by string or tuple
        if strXYZ is not None:
            cells = strXYZ.replace('(', '').replace(')', '').strip().split(',')
            x, y, z = float(cells[0]), float(cells[1]), float(cells[2])
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        elif tupXYZ is not None:
            x, y, z = tupXYZ  # [0], strXYZ[1],strXYZ[2]
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def getTup(self):  # return (x,y,z) as a tuple
        """
        Returns x,y,z as a tuple
        :return: tuple
        """
        return (self.x, self.y, self.z)

    def getStr(self, nPlaces=3):
        """
        Returns x,y,z as a string
        :param nPlaces:
        :return: string
        """
        return '{}, {}, {}'.format(round(self.x, nPlaces), round(self.y, nPlaces), round(self.z, nPlaces))

    def mag(self):  # normal way to calculate magnitude of a vector
        """
        Finds the magnitude of a vector
        :return: magnitude
        """
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def normalize(self):  # typical way to normalize to a unit vector
        """
        Normalizes the unit vector by using the calculated magnitude
        :return: l
        """
        l = self.mag()
        if l <= 0.0:
            return
        self.__idiv__(l)

    def getAngleRad(self):
        """
        Gets angle of position relative to an origin (0,0) in the x-y plane
        :return: angle in x-y plane in radians
        """
        l = self.mag()
        if l <= 0.0:
            return 0
        if self.y >= 0.0:
            return math.acos(self.x / l)
        return 2.0 * math.pi - math.acos(self.x / l)

    def getAngleDeg(self):
        """
        Gets angle of position relative to an origin (0,0) in the x-y plane
        :return: angle in x-y plane in degrees
        """
        return 180.0 / math.pi * self.getAngleRad()


class Material():
    def __init__(self, uts=None, ys=None, modulus=None, staticFactor=None):
        self.uts = uts
        self.ys = ys
        self.E = modulus
        self.staticFactor = staticFactor


class Node():
    def __init__(self, name=None, position=None):
        self.name = name
        self.position = position if position is not None else Position()

    def __eq__(self, other):
        """
        This overloads the == operator such that I can compare two nodes to see if they are the same node.  This is
        useful when reading in nodes to make sure I don't get duplicate nodes
        """
        if self.name != other.name:
            return False
        if self.position != other.position:
            return False
        return True

    def getName(self):
        """
        Returns a name
        :return: name
        """
        # The code for this code was copied from Dr.Smay's PipeNetwork_classes_stem.py,
        # and modified to fit this programs requirements
        return self.name


class Link():
    def __init__(self, name="", node1="1", node2="2", length=None, angleRad=None):
        """
        Basic definition of a link contains a name and names of node1 and node2
        """
        self.name = ""
        self.node1_Name = node1
        self.node2_Name = node2
        self.length = None
        self.angleRad = None

    def __eq__(self, other):
        """
        This overloads the == operator for comparing equivalence of two links.
        """
        if self.node1_Name != other.node1_Name: return False
        if self.node2_Name != other.node2_Name: return False
        if self.length != other.length: return False
        if self.angleRad != other.angleRad: return False
        return True

    def set(self, node1=None, node2=None, length=None, angleRad=None):
        """
        Sets node1, node2, length, and angleRad
        """
        self.node1_Name = node1
        self.node2_Name = node2
        self.length = length
        self.angleRad = angleRad

    def getName(self):
        """
        Returns a name
        :return: name
        """
        # The code for this code was copied from Dr.Smay's PipeNetwork_classes_stem.py,
        # and modified to fit this programs requirements
        return self.name


class TrussModel():
    def __init__(self):
        self.title = None
        self.links = []
        self.nodes = []
        self.material = Material()

    def getNode(self, name):
        """
        Gets the truss nodes
        :param name: name of node
        :return: n
        """
        for n in self.nodes:
            if n.name == name:
                return n


class TrussController():
    def __init__(self):
        self.truss = TrussModel()  # These simplify the reference for the truss classes
        self.view = TrussView()

    def ImportFromFile(self, data, TM=TrussModel()):
        """
        Data is the list of strings read from the data file.
        We need to parse this file and build the lists of nodes and links that make up the truss.
        Also, we need to parse the lines that give the truss title, material (and strength values).

        Reading Nodes:
        I create a new node object and then set its name and position.x and position.y values.  Next, I check to see
        if the list of nodes in the truss model has this node with self.hasNode(n.name).  If the trussModel does not
        contain the node, I append it to the list of nodes

        Reading Links:
        The links should come after the nodes.  Each link has a name and two node names.  See method addLink
        """
        # The code for this code was copied from Dr.Smay's PipeNetwork_classes_stem.py,
        # and modified to fit this programs requirements
        i = 0
        TM.links.clear()
        TM.nodes.clear()
        TM.title = None
        TM.material.uts = None
        TM.material.ys = None
        TM.material.E = None
        TM.material.staticFactor = 0

        while i < len(data):
            L = '' + data[i]
            L = L.lower().strip()
            # read in a pipe
            if L.find('#') == 0:
                n = 1
                pass
            elif L.find('title') >= 0:
                self.importTitle(data, i, TM)
                pass
            elif L.find('link') >= 0:
                # read in a pipe and increase i to end of pipe section
                self.importLink(data, i, TM)
                pass
            elif L.find('node') >= 0:
                self.importNode(data, i, TM)
                pass
            elif L.find('material') >= 0:
                self.importMaterial(data, i, TM)
                pass
            elif L.find('static_factor') >= 0:
                self.importSF(data, i, TM)
                pass
            i += 1

        self.calcLinkVals()
        self.displayReport()
        self.drawTruss()

    def importTitle(self, data, j, TM=TrussModel()):
        """
        Imports the title from the "Truss Design Inpot File.txt" for uses in the program
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        parts = data[j].strip().split()
        A = parts[1]
        B = parts[2]
        C = parts[3]
        self.truss.title = (A + " " + B + " " + C).strip("'")
        pass

    def importMaterial(self, data, j, TM=TrussModel()):
        """
        Imports the material from the "Truss Design Inpot File.txt" for uses in the program
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        parts = data[j].strip().split()
        self.truss.material.uts = float(parts[1].strip(','))
        self.truss.material.ys = float(parts[2].strip(','))
        self.truss.material.E = float(parts[3].strip(','))
        pass

    def importSF(self, data, j, TM=TrussModel()):
        """
        Imports the static factor from the "Truss Design Inpot File.txt" for uses in the program
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        parts = data[j].strip().split()
        self.truss.material.staticFactor = float(parts[1].strip(','))
        pass

    def importLink(self, data, j, TM=TrussModel()):
        """
        Imports the links from the "Truss Design Inpot File.txt" for uses in the program
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        L = Link()
        parts = data[j].strip().split()
        name = parts[1].strip(',')
        node1 = parts[2].strip(',')
        node2 = parts[3].strip(',')
        run = True
        for l in self.truss.links:
            if l.name == name:
                run = False
        if self.hasNode(node1) and self.hasNode(node2) and run == True:
            L.name = name
            L.node1_Name = node1
            L.node2_Name = node2
            self.addLink(L)
        pass

    def importNode(self, data, j, TM=TrussModel()):
        """
        Imports the nodes from the "Truss Design Input File.txt" for uses in the program
        """
        parts = data[j].strip().split()
        if len(parts) >= 4:
            name = parts[1]
            # Check if the coordinate strings can be converted to floats
            try:
                x_coord = float(parts[2].strip(','))
                y_coord = float(parts[3].strip(','))
            except ValueError:
                # If conversion fails, print an error message and skip this node
                print("Error: Invalid node coordinates for node", name)
                return

            # Create and add the node if conversion is successful
            if not self.hasNode(name):
                N = Node()
                N.name = name
                N.position.x = x_coord
                N.position.y = y_coord
                self.addNode(N)
        else:
            # If the input data doesn't have enough parts, print an error message
            print("Error: Invalid data format for node at line", j + 1)

    def hasNode(self, name):
        """
        Determines whether the file "Truss Design Input File.txt" contains nodes
        :param name: node
        :return: True or False
        """
        for n in self.truss.nodes:
            if n.name == name:
                return True
        return False

    def addNode(self, node):
        """
        Appends the nodes
        :return: nothing
        """
        self.truss.nodes.append(node)

    def getNode(self, name):
        """
        Gets the truss nodes
        :param name: name of node
        :return: n
        """
        for n in self.truss.nodes:
            if n.name == name:
                return n

    def addLink(self, link):
        """
        Appends the links
        :param link: truss link
        :return: nothing
        """
        self.truss.links.append(link)

    def calcLinkVals(self):
        """
        Calculates the link length values
        :return: nothing
        """
        for l in self.truss.links:
            n1 = None
            n2 = None
            if self.hasNode(l.node1_Name):
                n1 = self.getNode(l.node1_Name)
            if self.hasNode(l.node2_Name):
                n2 = self.getNode(l.node2_Name)
            if n1 is not None and n2 is not None:
                r = n2.position - n1.position
                l.length = r.mag()
                l.angleRad = r.getAngleRad()

    def setDisplayWidgets(self, args):
        """
        Displays the widgets
        :return: nothing
        """
        self.view.setDisplayWidgets(args)

    def displayReport(self):
        """
        Displays the report
        :return: nothing
        """
        self.view.displayReport(truss=self.truss)

    def drawTruss(self):
        """
        Draws the truss
        :return: nothing
        """
        self.view.buildScene(truss=self.truss)


class TrussView():
    """
    Gives the given parameters to build the truss view
    """

    def __init__(self):
        # setup widgets for display.  redefine these when you have a gui to work with using setDisplayWidgets
        self.scene = qtw.QGraphicsScene()
        self.le_LongLinkName = qtw.QLineEdit()
        self.le_LongLinkNode1 = qtw.QLineEdit()
        self.le_LongLinkNode2 = qtw.QLineEdit()
        self.le_LongLinkLength = qtw.QLineEdit()
        self.te_Report = qtw.QTextEdit()
        self.gv = qtw.QGraphicsView()

        # region setup pens and brushes and scene
        # make the pens first
        # a thick darkGray pen
        self.penLink = qtg.QPen(qtc.Qt.darkGray)
        self.penLink.setWidth(4)
        # a medium darkBlue pen
        self.penNode = qtg.QPen(qtc.Qt.darkBlue)
        self.penNode.setStyle(qtc.Qt.SolidLine)
        self.penNode.setWidth(1)
        # a pen for the grid lines
        self.penGridLines = qtg.QPen()
        self.penGridLines.setWidth(1)
        # I wanted to make the grid lines more subtle, so set alpha=25
        self.penGridLines.setColor(qtg.QColor.fromHsv(197, 144, 228, alpha=50))
        # now make some brushes
        # build a brush for filling with solid red
        self.brushFill = qtg.QBrush(qtc.Qt.darkRed)
        # a brush that makes a hatch pattern
        self.brushNode = qtg.QBrush(qtg.QColor.fromCmyk(0, 0, 255, 0, alpha=100))
        # a brush for the background of my grid
        self.brushGrid = qtg.QBrush(qtg.QColor.fromHsv(87, 98, 245, alpha=128))
        # endregion

    def setDisplayWidgets(self, args):
        """
        Displays the widgets
        """
        self.te_Report = args[0]
        self.le_LongLinkName = args[1]
        self.le_LongLinkNode1 = args[2]
        self.le_LongLinkNode2 = args[3]
        self.le_LongLinkLength = args[4]
        self.gv = args[5]
        self.gv.setScene(self.scene)

    def displayReport(self, truss=None):
        """
        Displays the report
        """
        if truss is None:
            print("Error: Truss object is not provided.")
            return

        self.te_Report.clear()  # Clear the text edit widget before updating

        st = '\tTruss Design Report\n'
        st += 'Title:  {}\n'.format(truss.title)
        st += 'Static Factor of Safety:  {:0.2f}\n'.format(truss.material.staticFactor)
        st += 'Ultimate Strength:  {:0.2f}\n'.format(truss.material.uts)
        st += 'Yield Strength:  {:0.2f}\n'.format(truss.material.ys)
        st += 'Modulus of Elasticity:  {:0.2f}\n'.format(truss.material.E)
        st += '____________________Link Summary_______________________\n'

        longest = None  # Initialize longest variable to None

        for l in truss.links:
            if longest is None or l.length > longest.length:
                longest = l

            st += '{}\t{}\t{}\t{:0.2f}\t{:0.2f}\n'.format(l.name, l.node1_Name, l.node2_Name, l.length, l.angleRad)

        if longest is not None:
            self.le_LongLinkName.setText(longest.name)
            self.le_LongLinkLength.setText("{:0.2f}".format(longest.length))
            self.le_LongLinkNode1.setText(longest.node1_Name)
            self.le_LongLinkNode2.setText(longest.node2_Name)
        else:
            # Handle the case where there are no links in the truss
            self.le_LongLinkName.clear()
            self.le_LongLinkLength.clear()
            self.le_LongLinkNode1.clear()
            self.le_LongLinkNode2.clear()

        self.te_Report.setText(st)

    def buildScene(self, truss=None):
        """
        Builds the scene the program widgets are displayed on
        """
        if truss is None:
            print("Error: Truss object is not provided.")
            return

        # Create a QRect() object to help with drawing the background grid.
        rect = qtc.QRect()
        rect.setTop(int(truss.nodes[0].position.y))  # Convert float to int
        rect.setLeft(int(truss.nodes[0].position.x))  # Convert float to int
        rect.setHeight(0)
        rect.setWidth(0)
        for n in truss.nodes:
            if n.position.y > rect.top():
                rect.setTop(int(n.position.y))  # Convert float to int
            if n.position.y < rect.bottom():
                rect.setBottom(int(n.position.y))  # Convert float to int
            if n.position.x > rect.right():
                rect.setRight(int(n.position.x))  # Convert float to int
            if n.position.x < rect.left():
                rect.setLeft(int(n.position.x))  # Convert float to int
        rect.adjust(-50, 50, 50, -50)

        # clear out the old scene first
        self.scene.clear()

        # draw a grid
        self.drawAGrid(DeltaX=10, DeltaY=10, Height=abs(rect.height()), Width=abs(rect.width()),
                       CenterX=rect.center().x(), CenterY=rect.center().y())
        # draw the truss
        self.drawLinks(truss=truss)
        self.drawNodes(truss=truss)

    def drawAGrid(self, DeltaX=10, DeltaY=10, Height=320, Width=180, CenterX=120, CenterY=60):
        """
        This makes a grid for reference.  No snapping to grid enabled.
        :param DeltaX: grid spacing in x direction
        :param DeltaY: grid spacing in y direction
        :param Height: height of grid (y)
        :param Width: width of grid (x)
        :param CenterX: center of grid (x, in scene coords)
        :param CenterY: center of grid (y, in scene coords)
        :param Pen: pen for grid lines
        :param Brush: brush for background
        :return: nothing
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications

        Pen = self.penGridLines
        Brush = self.brushGrid
        height = self.scene.sceneRect().height() if Height is None else Height
        width = self.scene.sceneRect().width() if Width is None else Width
        left = self.scene.sceneRect().left() if CenterX is None else (CenterX - width / 2.0)
        right = self.scene.sceneRect().right() if CenterX is None else (CenterX + width / 2.0)
        top = -1.0 * self.scene.sceneRect().top() if CenterY is None else (-CenterY + height / 2.0)
        bottom = -1.0 * self.scene.sceneRect().bottom() if CenterY is None else (-CenterY - height / 2.0)
        Dx = DeltaX
        Dy = DeltaY
        pen = qtg.QPen() if Pen is None else Pen

        # make the background rectangle first
        if Brush is not None:
            rect = qtw.QGraphicsRectItem(left, top, width, -height)
            rect.setBrush(Brush)
            rect.setPen(pen)
            self.scene.addItem(rect)
        # draw the vertical grid lines
        x = left
        while x <= right:
            lVert = qtw.QGraphicsLineItem(x, top, x, bottom)
            lVert.setPen(pen)
            self.scene.addItem(lVert)
            x += Dx
        # draw the horizontal grid lines
        y = bottom
        while y <= top:
            lHor = qtw.QGraphicsLineItem(left, y, right, y)  # now flip y
            lHor.setPen(pen)
            self.scene.addItem(lHor)
            y += Dy
        pass

    def drawLinks(self, truss=None, TM=TrussModel()):
        """
        This code draws the links between the node points
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        scene = self.scene
        penLink = self.penLink
        for l in truss.links:
            n1 = truss.getNode(l.node1_Name)
            n2 = truss.getNode(l.node2_Name)
            p1 = n1.position
            p2 = n2.position
            line = qtw.QGraphicsLineItem(p1.x, -p1.y, p2.x, -p2.y)
            # give the link a name for rollover behavior
            line.setData(0, ('Link: ' + l.getName()))
            # assign tool tip string
            line.setPen(penLink)
            # add link to scene
            scene.addItem(line)
            # self.drawALabel((p1.x+0.5*(p2.x-p1.x)),(-p2.y+0.5*(p2.y-p1.y)),str=l.name,pen=self.penLink,brush=None)
        pass

    def drawNodes(self, truss=None, scene=None, TM=TrussModel()):
        """
        Draws a circle for each node along with a label and creates the tool tip.
        Also, draws an arrow for external flow.
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        if scene is None:
            scene = self.scene
        penNode = self.penNode
        brushNode = self.brushNode
        penNodeOutline = qtg.QPen() if penNode is None else penNode
        penNodeLabel = qtg.QPen(qtc.Qt.darkMagenta)
        brushNodeFill = qtg.QBrush() if brushNode is None else brushNode
        for n in truss.nodes:
            x = n.position.x
            y = n.position.y
            c = 0
            if n.name == 'Left':
                c = 1
            if n.name == 'Right':
                c = 10
            self.drawACircle(x, y, 7, brush=brushNodeFill, pen=penNodeOutline, name=('node: ' + n.getName()))
            self.drawALabel(x - (25 + c), y + 30, str=n.getName(), pen=penNodeLabel)
        pass

    def drawALabel(self, x, y, str='', pen=None, brush=None, tip=None):
        """
        I've decided that x,y are the center of the label.  Find corner based on label width and height.
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        scene = self.scene
        lbl = qtw.QGraphicsTextItem(str)
        w = lbl.boundingRect().width()
        h = lbl.boundingRect().height()
        lbl.setX(x)  # lbl.setX(x - w / 2.0)
        lbl.setY(-y)  # lbl.setY(-y - h / 2.0)
        if tip is not None:
            lbl.setToolTip(tip)
        if pen is not None:
            lbl.setDefaultTextColor(pen.color())
        if brush is not None:
            # this makes a nice background
            bkg = qtw.QGraphicsRectItem(lbl.x(), lbl.y(), w, h)
            bkg.setBrush(brush)
            outlinePen = qtg.QPen(brush.color())
            bkg.setPen(outlinePen)
            scene.addItem(bkg)
        scene.addItem(lbl)
        pass

    def drawACircle(self, centerX, centerY, Radius, angle=0, brush=None, pen=None, name=None, tooltip=None):
        """
        Creates a circle with specified radius and centering
        :param centerX: center of grid (x, in scene coords)
        :param centerY: center of grid (y, in scene coords)
        :param Radius: radius of circle
        :param angle: angle of text
        :param brush: brush for background
        :param pen: pen for outline
        :param name: name of node
        :param tooltip: displays node name when cursor is hovering over it
        :return: nothing
        """
        # The code was inspired or copied from Dr.Smay's PipeNetwork_classes_stem.py,and modified to
        # fit the code specifications
        scene = self.scene
        ellipse = qtw.QGraphicsEllipseItem(centerX - Radius, -1.0 * (centerY + Radius), 2 * Radius, 2 * Radius)
        if pen is not None:
            ellipse.setPen(pen)
        if brush is not None:
            ellipse.setBrush(brush)
        if name is not None:
            ellipse.setData(0, name)
        if tooltip is not None:
            ellipse.setToolTip(tooltip)
        scene.addItem(ellipse)
        pass
