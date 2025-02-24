# Data Structures
from copy import copy
from itertools import *
class Error(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.message=message
        self.code=code
    
    def __str__(self) -> str:
        return f'Error Code {self.code}: {self.message}'

class MathLogic:
    def prod(list1):
        """
        Returns the product of the integer/float values of a 1D List.
        Returns a float or integer.
        """
        result=1
        for item in list1:
            if type(item)==int or type(item)==float:
                result*=item
            else:
                print(Error("Math01","Product of list can only be done with integer or float items"))
                return -1
        return result

class Matrix:
    def __init__(self,rows=1,columns=1,data=[]):
        if columns<=0 or rows<=0:
            # Error message for invalid input
            print("Error - Matrix cannot have size less than or equal to 0")
        
        else:
            # Keep as constants
            self.columns=columns
            self.rows=rows
            #matrix of size rows * columns
            self.matrix=[[0 for column in range(columns)] for row in range(rows)] 

    def __setattr__(self, name, value):
        match name:
            case "matrix":
                print(value)
                if not (len(value) == self.rows and all([len(row) == self.columns for row in value])):
                    self.rows, self.columns = len(value), len(value[0])
                object.__setattr__(self,name,value)
            case _:
                object.__setattr__(self,name,value)

    def __str__(self):
        result=""
        for row in self.matrix:
            result+=str(row)+"\n"
        return result
            
    def __add__(self,m2):
        """
        Preforms logic of addition between matrices of any size. 
        This requires the size of the matrices to be the same. 
        """
        if m2.rows==self.rows and m2.columns==self.columns: #checks for whether if it is valid size matrix
            result=Matrix(self.rows,self.columns)
            result.matrix=[[self.matrix[row][column]-m2.matrix[row][column] for column in range(self.columns)] for row in range(self.rows)] 
            return result
        else:
            print(Error("Mat_01_a","Invalid addition of two matrices of different sizes"))
            return -1

    def __sub__(self,m2):
        """
        Preforms logic of subtraction between matrices of any size. 
        This requires the size of the matrices to be the same. 
        """
        if m2.rows==self.rows and m2.columns==self.columns: #checks for whether if it is valid size matrix
            result=Matrix(self.rows,self.columns)
            result.matrix=[[self.matrix[row][column]-m2.matrix[row][column] for column in range(self.columns)] for row in range(self.rows)]
            return result
        else:
            print(Error("Mat_01_b","Invalid subtraction of two matrices of different sizes"))
            return -1

    def __mul__(self,m2):
        """
        Preforms logic of multiplication between matrices of any size. 
        This requires the number of rows of the first matrix to be equal to the number of columns of the second matrix. 
        """
        #check if it is a valid multiplication, requiring a square matrix:
        if m2.rows==self.columns:
            # matrix multiplication logic
            #   | a b | | e f |   =   | ea+gb fa+hb |
            #   | c d | | g h |       | ec+gd fc+hd |
            
            # final result should be a matrix of same size as the previous matrices
            result=Matrix(m2.rows,self.columns)
        
            # for each coordinate:
            # starting from column 0 in matrix 2 and going up (count) and starting from row 0 and going up for matrix 1(count)
            # adds up the sum of the products of each coordinate across the row and columns, intersecting the coordinate in the final result
                                # finds the product of each corrosponding row and column in both matrices
            result.matrix = [[sum([self.matrix[row][i]*m2.matrix[i][column] for i in range(0,result.rows)]) for column in range(m2.columns)] for row in range(self.rows)]
                                                                                                        #  seperates into 2d list of columns and rows
            return result
        else:
            print(Error("Mat_02","Invalid multiplication operation of two non-square matrices: Invalid matrix size"))
            return -1
    
    def isVector(self):
        """
        Checks if the object is a column or row vector.
        """
        if (self.columns==1 or self.rows==1) and self.columns!=self.rows:
            return True
        else:
            return False
    
    def convertColumnToRow(self):
        """
        Converts column vectors(nx1 matrix) to row vectors(1xn matrix)
        """
        if self.isVector() and self.columns==1:
            self.matrix=[[i for item in self.matrix for i in item]]
        else:
            print(Exception("Mat_04","Vector is already row vector or is a matrix"))

    def addRows(self, count : int = 1):
        """
        Adds rows to the matrix. count must be a non zero integer.
        """
        if count>0:
            self.rows+=count
            self.matrix.append([0 for column in self.columns] for row in count)
        elif count<0:
            self.delRows(count*-1)
        
    def delRows(self, count: int = 1):
        if count>0:
            self.rows-=count
            self.matrix.append([0 for column in self.columns] for row in count)
        elif count<0:
            self.addRows(count*-1)
        
    #def inverse(self):

    def swap_rows(self,r1,r2): 
        """
        Swaps the rows given in the two parameters passed in, r1, r2.
        Modifies the matrix itself, returns None
        """
        self.matrix[r1], self.matrix[r2] = self.matrix[r2], self.matrix[r1]

    def REF(self) -> tuple:
        """
        Preforms gaussian elimination on matrix to produce a row echelon matrix.
        """

        result=copy(self)
        swapped_rows=0
        column=0

        for row in range(result.rows):
            #move up depending if rows have been swapped:
            row-=swapped_rows
            pivot=result.matrix[row][column]
            
            #if pivot chosen is 0:
            while pivot==0:
                found_pivot=False
                for i in range(row+1, result.rows):
                    if result.matrix[i][column]!=0:
                        result.swap_rows(((row)%result.rows),((i)%result.rows))     #swap the row that is suitable with the row with approprate pivot
                        swapped_rows+=1
                        found_pivot=True
                        pivot=result.matrix[row][column]
                        break
                if not found_pivot:
                    #move column to right by one
                    column+=1
                    if column>=result.columns:
                        #if all the below rows are 0s:
                        return result, -1 ** swapped_rows
                    continue
                    
        
            for i in range(row+1,result.rows): # loop through all the rows below the pivot is 
                #if the bottom rows is 0, skip
                if sum(result.matrix[i])==0:
                    continue
                #factor to multiply the row with
                factor=result.matrix[i][column]/pivot
                for j in range(column+1,result.columns): #reduce starting from the column after the column under the pivot
                    result.matrix[i][j]-=result.matrix[row][j]*factor
                result.matrix[i][column]=0

            #increment column count by 1 if successful pivot has been found
            if column+1 < self.columns: # if possible, try to move to next column
                column+=1
        return result, -1 ** swapped_rows

    #def RREF

    def get_diagonal(m1) -> list:
        """Returns 1D list of the diagonal of the matrix."""
        result=[]
        for i in range(max([m1.columns,m1.rows])):
            result.append(m1.matrix[i][i])
        return result
    
    def get_determinant(self):
        """
        Returns the determinant of the matrix via Gaussian elimination.
        """
        # Determinant is the number by which an area/volume would be scaled by
        if self.columns==self.rows:
            echelon=self.REF()
            diagonal=echelon[0].get_diagonal()
            return MathLogic.prod(diagonal)*echelon[1]
        else:
            print(Error("Mat_03","Invalid get_determinant operation: Non-square matrices do not have a determinant"))
            return -1
    
    #dot product
    def dot(v1,v2):
        #check for whether if m1 and m2 are vectors:
        if v1.isVector() and v2.isVector() and (v1.columns==v2.rows or v1.rows==v2.columns):
            v1.convertColumnToRow()
            v2.convertColumnToRow()
            return sum(v1.matrix[0][i]*v2.matrix[0][i] for i in range(v1.columns))
        else:
            return v1*v2
    #def get_dot_product(self):
