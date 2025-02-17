# Data Structures
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
    #    result=""
    #    for row in self.matrix:
    #        result+="|"
    #        for column in row:
    #            result+=" "+str(column)+" "
    #        result+="|\n"
    #    return result
                
            
    def __add__(self,m2):
        result=Matrix(self.rows,self.columns)
        for column in range(0,self.columns,1):
            #making the first column vector:
            for row in range(0,self.rows,1):
                #for each coordinate:
                result[row][column]=self.matrix[row][column]+m2.matrix[row][column]
        return result

    def __sub__(self,m2):
        result=Matrix(self.rows,self.columns)
        for column in range(0,self.columns,1):
            #making the first column vector:
            for row in range(0,self.rows,1):
                #for each coordinate:
                result[row][column]=self.matrix[row][column]-m2.matrix[row][column]
        return result

    def __mul__(self,m2):
        #check if it is a valid multiplication:
        if (self.rows == m2.columns and self.columns == m2.rows) or (self.columns == m2.rows and self.rows == m2.columns):
            # matrix multiplication logic
            #   | a b | | e f |   =   | ea+gb fa+hb |
            #   | c d | | g h |       | ec+gd fc+hd |
            
            # final result should be a matrix of same size as the previous matrices
            result=Matrix(min(self.rows,m2.rows),(min(self.columns,m2.columns)))
            for column in range(0,max(self.columns,m2.columns),1):
                #making the first column vector:
                for row in range(0,max(self.rows,m2.rows),1):
                    #for each coordinate:
                    #row=0,column=0
                    sum=0
                    for count in range(max(self.columns,m2.columns)):
                        #count=1
                        #starting from column 0 in matrix 2 and going up (count) and starting from row 0 and going up for matrix 1(count)
                        sum+=self.matrix[row-1][count-1]*m2.matrix[count-1][column-1]
                    
                    result.matrix[row-1][column-1]=sum
            return result
        else:
            print("Invalid multiplication operation of two matrices: not the same size")

    #normalization function
    def normalize(self):
        pass
    #determinant function

    #dot product
m1=Matrix(2,3)
m1.matrix=[[0,-2,2],
           [5,1,5]]

m2=Matrix(3,2)
m2.matrix=[[0,1],
           [3,4],
           [6,7],]

m3 = Matrix(3,3)
m3.matrix=[[1,2,3],[4,5,6],[7,8,9]]

m4 = Matrix(3,3)
m4.matrix=[[1,2,3],[4,5,6],[7,8,9]]
print(m1)
print(m2)

#why is this printing something extra?
print("result:",m3*m4)
