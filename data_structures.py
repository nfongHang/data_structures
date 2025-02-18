# Data Structures
from copy import copy
import math
import random


class Error(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.message=message
        self.code=code
    
    def __str__(self) -> str:
        return f'Error Code {self.code}: {self.message}'


class Matrix:
    def __init__(self,columns=1,rows=1,data=[]):
        if columns==0 or rows==0:
            # Error message for invalid input
            print("Error - Matrix cannot have size 0")
        
        else:
            self.matrix=[]

            # Keep as constants
            self.columns=columns
            self.rows=rows

            # For each row there is:
            for column in range(0,columns):
                #append a fixed size array
                self.matrix.append([0]*rows)
    
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
            for column in range(0,self.columns,1):
                for row in range(0,self.rows,1):
                    #for each coordinate:
                    result.matrix[row][column]=self.matrix[row][column]+m2.matrix[row][column]
            return result
        else:
            return Error("Mat_01","Invalid addition of two matrices of different sizes")

    def __sub__(self,m2):
        """
        Preforms logic of subtraction between matrices of any size. 
        This requires the size of the matrices to be the same. 
        """
        if m2.rows==self.rows and m2.columns==self.columns: #checks for whether if it is valid size matrix
            result=Matrix(self.rows,self.columns)
            for column in range(0,self.columns,1):
                for row in range(0,self.rows,1):
                    #for each coordinate:
                    result.matrix[row][column]=self.matrix[row][column]-m2.matrix[row][column]
            return result
        else:
            return Error("Mat_01","Invalid subtraction of two matrices of different sizes")

    def __mul__(self,m2):
        """
        Preforms logic of multiplication between matrices of any size. 
        This requires the number of rows of the first matrix to be equal to the number of columns of the second matrix. 
        """
        #check if it is a valid multiplication:
        if m2.rows==self.columns:
            # matrix multiplication logic
            #   | a b | | e f |   =   | ea+gb fa+hb |
            #   | c d | | g h |       | ec+gd fc+hd |
            
            # final result should be a matrix of same size as the previous matrices
            result=Matrix(m2.rows,self.columns)
            for column in range(m2.columns):
                #making the first column vector:
                for row in range(self.rows):
                    #for each coordinate:
                    #row=0,column=0
                    sum=0
                    for count in range(self.rows):
                        #count=1
                        #starting from column 0 in matrix 2 and going up (count) and starting from row 0 and going up for matrix 1(count)
                        sum+=self.matrix[row-1][count-1]*m2.matrix[count-1][column-1]
                    
                    result.matrix[row-1][column-1]=sum
            return result
        else:
            return Error("Mat_02","Invalid multiplication operation of two non-square matrices: Invalid matrix size")

    def swap_rows(self,r1,r2) -> None: 
        """
        Swaps the rows given in the two parameters passed in, r1, r2.
        Modifies the matrix itself, returns None
        """
        self.matrix[r1], self.matrix[r2] = self.matrix[r2], self.matrix[r1]

    def gaussian_elimination(self) -> tuple:
        """
        Preforms gaussian elimination on matrix to produce a row echelon matrix.
        Note: PLEASE FIX NONSQUARE MATRIX NOT WORKING
        """
        result=copy(self)
        swapped_rows=0
        column=0
        for row in range(result.rows):
            #move up depending if rows have been swapped:
            row-=swapped_rows

            pivot=result.matrix[row][column]

            found=None
            
            #if pivot chosen is 0:
            if pivot==0:
                found=False #flag for whether if a second suitable pivot for the same column in different rows has been chosen
                while not found:
                    for i in range(row+1, result.rows):
                        if result.matrix[i][column]!=0:
                            result.swap_rows(((row)%result.rows),((i)%result.rows))     #swap the row that is suitable with the row with approprate pivot
                            swapped_rows+=1
                            found=True
                            pivot=result.matrix[row][column]
                            break
                    if not found:
                        #move column to right by one
                        if column+1<result.columns:
                            #skip the column and move to the next
                            column+=1
                        else:
                            #if all the below rows are 0s:
                            found=-1
            if found==None:
                for i in range(row+1,result.rows): # loop through all the rows below the pivot is 
                    ##print('a')
                    #if the bottom rows is 0, skip
                    if sum(result.matrix[i])!=0:
                        for j in range(column+1,result.columns): #starting from the column after the column under the pivot
                            result.matrix[i][j]=result.matrix[i][j]-result.matrix[row][j]*result.matrix[i][column]/pivot
                            ##print(result)
                        result.matrix[i][column]=0
                #increment column count by 1 if successful pivot has been found
                column+=1
            elif found==-1:
                break
            
        return result, int(not(swapped_rows%2))*2-1

    def get_diagonal(m1) -> list:
        result=[]
        for i in range(max([m1.columns,m1.rows])):
            result.append(m1.matrix[i][i])
        return result
    
    def get_determinant(self):
        # Determinant is the number by which an area/volume would be scaled by
        if self.columns==self.rows:
            gaussian=self.gaussian_elimination()
            diagonal=gaussian[0].get_diagonal()
            print(gaussian[1])
            return math.prod(diagonal)*gaussian[1]
        else:
            return Error("Mat_03","Invalid get_determinant operation: Non-square matrices do not have a determinant")

    #dot product
