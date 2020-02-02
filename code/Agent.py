# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image,ImageChops
import numpy as np
import ImageUtil

UNKNOWN = -1
DEBUG = 0
DIFF_THRESH = 2
MIN_OPTION_DIFF_THRESH = 5


class rpmFrame:
    def __init__(self,name,figure):
        #print "In rpmFrame init :  ", name, figure.visualFilename
        self.name = name
        self.image_filename = figure.visualFilename
        self.image = Image.open(figure.visualFilename)  # original image
        self.im_np = ImageUtil.binarize(self.image)     # Image bitmap in np array
        self.object_count = len(figure.objects)
        #attributes={}

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.input_frames={}
        self.option_frames={}
        self.option_image_list=[]
        pass

        
    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        answer = -1
        try :
            self.load_data(problem)
            
            if problem.problemType == '2x2' :
                answer = self.solve2x2(problem)
            elif problem.problemType == '3x3' :
                answer = self.solve3x3(problem)  ## stub for Project-2
            else :
                print "Unknown Problem Type : ", problem.problemType
                    
            #print " newV FINAL ANSWER : " , answer
        except BaseException :
            pass
        
        return answer      
    



    #******************************************************************************
    # Handler for 2x2 RPM 
    #******************************************************************************
    def solve2x2(self,problem):
                
        answer = self.isIdentical('A','B','C')
        if answer != UNKNOWN  : return answer
        
        answer = self.isIdentical('A','C','B')
        if answer != UNKNOWN  : return answer
            
        answer = self.isReflected('A','B','C')
        if answer != UNKNOWN  : return answer
        
        answer = self.isReflected('A','C','B')
        if answer != UNKNOWN  : return answer
            
        answer = self.isRotated('A','B','C')
        if answer != UNKNOWN  : return answer
        
        answer = self.isRotated('A','C','B')
        if answer != UNKNOWN  : return answer
            
        answer = self.isDiffConstant('A','B','C')
        if answer != UNKNOWN  : return answer

        answer = self.isDiffConstant('A','C','B')
        if answer != UNKNOWN  : return answer  
       
        answer = self.isFill('A','B','C')
        if answer != UNKNOWN  : return answer  

        answer = self.isFill('A','C','B')
        if answer != UNKNOWN  : return answer  
#        
#        #last resort  - check by object count
#        answer = self.checkByObjCount('A','B','C')
#        if answer != UNKNOWN  : return answer
        
        #print "coudln't find an answer. skipping "
        

        return -1    

    #******************************************************************************
    # getImage
    #******************************************************************************
    def getImage(self,frame_key):
        if frame_key.isalpha():
            return self.input_frames[frame_key].image
        else:
            return self.option_frames[frame_key].image
 
    #******************************************************************************
    # get image bitmap (numpy array)
    #******************************************************************************
    def getImgNp(self,frame_key):
        if frame_key.isalpha():
            return self.input_frames[frame_key].im_np
        else:
            return self.option_frames[frame_key].im_np
            
    #******************************************************************************
    # isIdentical :  if x=y find z=?
    #******************************************************************************
    def isIdentical(self,f1,f2,f3):
        try:
            im_x = self.getImage(f1)
            im_y = self.getImage(f2)
            im_z = self.getImage(f3)

            diff_xy = ImageUtil.find_image_diff(im_x, im_y)
            #print "isIdentical : diff_" , f1, f2 , " = " , diff_xy
            if diff_xy < DIFF_THRESH :
                option_diff_list=[]
                for i in range(1,7):
                    option_image = self.getImage(str(i))
                    option_diff = ImageUtil.find_image_diff(im_z, option_image )
                    option_diff_list.append(option_diff)
                min_diff = min(option_diff_list)
                min_index = option_diff_list.index(min_diff)
                if DEBUG : print "isIdentical : diff_xy=",diff_xy , " min_value= " , min_diff , " min_index =", min_index+1
                
                if(min_diff < MIN_OPTION_DIFF_THRESH):
                    return min_index+1
        
        except BaseException :
            print "Exception in isIdentical: ", f1,f2,f3
            pass   
        
        return -1
 
    #******************************************************************************
    # isRotated :45,90,135,180,225,270,315
    #******************************************************************************
    def isRotated(self,f1,f2,f3):
        try :
            im_x = self.getImage(f1)
            im_y = self.getImage(f2)
            im_z = self.getImage(f3)
    
            degree =[x*45 for x in range(1,8)]
            
            for d in degree :
                rot_x = im_x.rotate(d)
                diff_xy = ImageUtil.find_image_diff(rot_x, im_y) 
                #print "check rotation : diff_" , f1, f2 , " = " , diff_xy , "Degree= ", d
                
                if diff_xy < DIFF_THRESH+1 :
                    option_diff_list=[]
                    rot_z = im_z.rotate(d)
                    for i in range(1,7):
                        option_image = self.getImage(str(i))
                        option_diff = ImageUtil.find_image_diff(rot_z, option_image )
                        option_diff_list.append(option_diff)
                    min_diff = min(option_diff_list)
                    min_index = option_diff_list.index(min_diff)
                    
                    if DEBUG : print "isRotated : diff_xy=",diff_xy , " min_value= " , min_diff , " min_index =", min_index+1
                    
                    if(min_diff < MIN_OPTION_DIFF_THRESH):
                        return min_index+1        
        except BaseException :
            print "Exception in isRotated: ", f1,f2,f3
            pass  
        
        return -1

    #******************************************************************************
    # isReflected
    #******************************************************************************
    def isReflected(self,f1,f2,f3):
        res = self.check_reflection(f1,f2,f3 ,'x')
        if res == UNKNOWN:
            res = self.check_reflection(f1,f2,f3 ,'y')
        return res    
    
    def check_reflection(self,f1,f2,f3, axis):
        try :
            im_x = self.getImage(f1)
            im_y = self.getImage(f2)
            im_z = self.getImage(f3)
            
            if(axis == 'y'):
                transpose_x = im_x.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                transpose_x = im_x.transpose(Image.FLIP_TOP_BOTTOM)
               
            diff_xy = ImageUtil.find_image_diff(transpose_x, im_y)
            #print "check_reflection : diff_" , f1, f2 , " = " , diff_xy , "axis = ", axis
            
            if diff_xy < DIFF_THRESH :
                option_diff_list=[]
                if(axis == 'y'):
                    transpose_z = im_z.transpose(Image.FLIP_LEFT_RIGHT)
                else:
                    transpose_z = im_z.transpose(Image.FLIP_TOP_BOTTOM)
                
                for i in range(1,7):
                    option_image = self.getImage(str(i))
                    option_diff = ImageUtil.find_image_diff(transpose_z, option_image)
                    option_diff_list.append(option_diff)
                min_diff = min(option_diff_list)
                min_index = option_diff_list.index(min_diff)
               
                #print option_diff_list
                if DEBUG :print "isReflected : diff_xy=",diff_xy , " min_value= " , min_diff , " min_index =", min_index+1
                
                if(min_diff < MIN_OPTION_DIFF_THRESH):
                    return min_index+1  
        
        except BaseException :
            print "Exception in check_reflection: ", f1,f2,f3,axis
            pass  
        
        return -1

   #******************************************************************************
   #  Check if Images differ by a constant : PIL version
   #******************************************************************************
    def xx_isDiffConstant(self,f1,f2,f3):
        try :
            im_x = self.getImage(f1)
            im_y = self.getImage(f2)
            im_z = self.getImage(f3)
            
            image_delta_1 = ImageChops.invert(ImageChops.difference(im_x, im_y))
            # Find delta between delta_1 and im_x and compare it with im_y 
            image_delta_2 = ImageChops.invert(ImageChops.difference(im_x, image_delta_1))
            
            diff_xy = ImageUtil.find_image_diff( image_delta_2, im_y)
            print "x_isDiffConstant : diff_" , f1, f2 , " = " , diff_xy
            
            if diff_xy < DIFF_THRESH :
                option_diff_list=[]
                for i in range(1,7):
                    option_image = self.getImage(str(i))
                    d1 = ImageChops.invert(ImageChops.difference(im_z, option_image))
                    d2 = ImageChops.invert(ImageChops.difference(im_z, d1)) 
                    option_diff = ImageUtil.find_image_diff(d2, option_image )
                    option_diff_list.append(option_diff)
                min_diff = min(option_diff_list)
                min_index = option_diff_list.index(min_diff)
                print option_diff_list
                print "answer is " , min_index+1 
                
                if(min_diff < MIN_OPTION_DIFF_THRESH):
                    return min_index+1
        except BaseException :
                pass  
        
        return -1
        
    #******************************************************************************
    #  Check if Images differ by a constant : Numpy version
    #******************************************************************************  
    def isDiffConstant(self,f1,f2,f3):
        try :
            np1 = self.getImgNp(f1)
            np2 = self.getImgNp(f2)
            np3 = self.getImgNp(f3)
            
            diff_matrix_12 = ImageUtil.get_diff_matrix(np1 ,np2)         
            #print "isDiffConstant : diff_" , f1, f2 , 
    
            option_diff_list=[]
            for i in range(1,7):
                option_np = self.getImgNp(str(i))
                diff_matrix_3i = ImageUtil.get_diff_matrix(np3 ,option_np)  
                option_diff = ImageUtil.find_diff(diff_matrix_12, diff_matrix_3i)
                option_diff_list.append(option_diff)
            min_diff = min(option_diff_list)
            min_index = option_diff_list.index(min_diff)
            #print option_diff_list
            if DEBUG : print "isDiffConstant : min_value = " , min_diff , "min_index =", min_index+1 
            
            if(min_diff*100 < MIN_OPTION_DIFF_THRESH):
                return min_index+1
        except BaseException :
            print "Exception in isDiffConstant: ", f1,f2,f3
            pass
        
        return -1      
        
    #******************************************************************************
    #  Check pixel cnt ratio . Might have to enhance this function with 
    #    blk_pixel_interesection ratio
    #****************************************************************************** 
    def isFill(self,f1,f2,f3):
        try :
            im_x = self.getImage(f1)
            im_y = self.getImage(f2)
            im_z = self.getImage(f3)
            
            pixel_ratio_xy = ImageUtil.get_blk_pixel_ratio(im_x ,im_y) 
            intx_ratio_xy = ImageUtil.get_blk_intersection_ratio(im_x, im_y)        
            #print " isFill : diff_" , f1, f2 , "pixel_ratio=", pixel_ratio_xy , "intx_ratio=" , intx_ratio_xy
    
            option_diff_list=[]
            intx_diff_list=[]
            temp=[]
            temp2=[]
            for i in range(1,7):
                option_image = self.getImage(str(i))
                pixel_ratio_ci = ImageUtil.get_blk_pixel_ratio(im_z ,option_image) 
                ratio_diff = abs(pixel_ratio_xy - pixel_ratio_ci)
                option_diff_list.append(ratio_diff)
                temp.append(pixel_ratio_ci)
                
                ## intx ratio
                intx_ratio_ci = ImageUtil.get_blk_intersection_ratio(im_z ,option_image) 
                intx_diff = abs(intx_ratio_xy - intx_ratio_ci)
                intx_diff_list.append(intx_diff)
                temp2.append(intx_ratio_ci)
                
            min_diff = min(option_diff_list)
            min_index = option_diff_list.index(min_diff)
            
    #        print temp
    #        print option_diff_list
    #        print "isFill : min_value = " , min_diff , "min_index =", min_index+1 
    #        
    #        print temp2
    #        print intx_diff_list , intx_diff_list.index(min(intx_diff_list))+1
            
            if(min_diff < MIN_OPTION_DIFF_THRESH):
                return min_index+1
        
        except BaseException:
            print "Exception in isFill: ", f1,f2,f3
            pass
        
        return -1 
        
    
        
    #******************************************************************************
    # Handler for 3x3 RPM 
    #******************************************************************************
    def solve3x3(self,problem) :
        #print "3x3 solver coming soon "
        return -1
        
        
        
        
    #******************************************************************************
    # load_data
    #******************************************************************************
    def load_data(self, problem):
        try :
            if problem.problemType == '2x2' :
                
                if DEBUG : print problem.name
    #            self.input_frames['A'] = rpmFrame('A',problem.figures['A'])
    #            self.input_frames['B'] = rpmFrame('B',problem.figures['B'])
    #            self.input_frames['C'] = rpmFrame('C',problem.figures['C'])
    #            self.option_frames['1'] = rpmFrame('1',problem.figures['1'])
    #            self.option_frames['2'] = rpmFrame('2',problem.figures['2'])
    #            self.option_frames['3'] = rpmFrame('3',problem.figures['3'])
    #            self.option_frames['4'] = rpmFrame('4',problem.figures['4']) 
    #            self.option_frames['5'] = rpmFrame('5',problem.figures['5'])
    #            self.option_frames['6'] = rpmFrame('6',problem.figures['6'])
                                                   
                fig_keys = problem.figures.keys()
                for i in fig_keys:
                    if i.isalpha():
                        i=i.upper()
                        self.input_frames[i] = rpmFrame(i,problem.figures[i])
                    else :
                        self.option_frames[i] = rpmFrame(i,problem.figures[i])
                
    #            for name,figure in problem.figures.iteritems():
    #                
    #                frame = rpmFrame(name,figure)
    #                print "figure name : " , name , "|", figure , "||", frame
    #                
    #                if name.isalpha():
    #                    self.input_frames['name'] = frame
    #                    #print name,  self.input_frames['name']
    #                elif name.isdigit():
    #                    self.option_frames['name'] = frame
    #                    #print name,  self.input_frames['name']
    #                else:
    #                    print "Error object name"
                
#                # check if input is correctly stored
#                for k,v in self.input_frames.iteritems():
#                    print "RPM Frame " , v.name , "\t object_count ="  , v.object_count , "\t", v.image_filename
#                    #v.image.show()
#                for k,v in self.option_frames.iteritems():
#                    print "RPM Frame " , v.name , "\t object_count ="  , v.object_count ,"\t", v.image_filename 
           
        except BaseException:
            pass
           
        
        
    #******************************************************************************
    # Helper code for verbal solution
    #******************************************************************************
    def solve2x2_verbal(self, problem):
        if(problem.name == 'Basic Problem B-05' ) :
             print " reached solve : "  + problem.name +  " : "  +  problem.problemType + ": "  + problem.problemSetName 

             for k,v in problem.figures.iteritems():
                 print "key = ", k , " figure name = ", v.name   # v is Ravens Figure
                 for k1,v1 in v.objects.iteritems() : 
                     print "key  = ", k1 , " Object.name = ", v1.name  # v1 is Raven's Object
                     for k2,v2 in v1.attributes.iteritems():
                         print "attribute : " , k2 ,  "value = " , v2
                     
             # find num of objects in A and B
             print " Object count for A = " , len(problem.figures['A'].objects)
             print " Object count for B = " , len(problem.figures['B'].objects) 
             print " is Frame A same as B same ? " + str(cmp(problem.figures['A'].objects,problem.figures['B'].objects))
             
             # if number of objects are same , then compare attributes
             #A_obj1_attr = problem.figures['A'].objects['a'].attributes  # dictionary
             #B_obj1_attr = problem.figures['B'].objects['b'].attributes
             #res = cmp(A_obj1_attr, B_obj1_attr)
             #print " are attributes same ? " + str(res)
             
             objMap_AB = self.getObjectMapping(problem.figures['A'], problem.figures['B'])
             objMap_AC = self.getObjectMapping(problem.figures['A'], problem.figures['C'])
             #print objMap_AB
             #print objMap_AC
             trans_AB = self.getTransformation(problem.figures['A'] , problem.figures['B'], objMap_AB)
             trans_AC = self.getTransformation(problem.figures['A'] , problem.figures['C'], objMap_AC)
   
          
    def getTransformation(self,frame1, frame2, objMap):
        transformation = {'obj_cnt_changed':'', 'obj_deleted': -1, 'obj_added':-1 } 
        #{'shape'= '', 'shade' = '', 'fill' = '' , 'alignement' = '', 'angle' = -1 }
        
        obj_cnt_diff = len(frame1.objects) - len(frame2.objects)        
        if obj_cnt_diff == 0 :
            transformation['obj_cnt_changed'] = 'no'
        else :
            transformation['obj_cnt_changed'] = 'yes' 
            if obj_cnt_diff > 0:
                transformation['obj_deleted'] = diff
            else :
                transformation['obj_added'] = abs(diff)
                      
        for pair in objMap :
            x = frame1.objects[pair[0]]
            y = frame2.objects[pair[1]]
            
        for k, v in x.attributes.iteritems():
            #print "comparing attribute = " , k ,  "for objects : " , x.name , y.name
            if(k in x.attributes and k in y.attributes):          
                if x.attributes[k] == y.attributes[k]:
                    transformation[k] = 'same'
                else:  
                    if(str.lower(k) == 'angle') : 
                        transformation[k] = abs(int(x.attributes[k]) - int(y.attributes[k]))
                    
                    elif(str.lower(k) == 'fill'):
                        if(str.lower(x.attributes[k]) != 'yes' or str.lower(x.attributes[k]) != 'no'):
                            print "Unexpected fill value " , x.attributes[k] , y.attributes[k]
                    
                    elif(str.lower(k) == 'alignment'): 
                        transformation[k] = x.attributes[k] + "|" +  y.attributes[k]
                    
                    else:
                        transformation[k]= 'diff'
        
        #printDict(transformation) 
        print "Transformation :" , frame1.name , frame2.name
        
        for k,v in transformation.iteritems():
            print "Key[] " , k , "| value = " , v
        
        return transformation         

    def compareAttributes(self,obj1, obj2):
        score =0
        for k, v in obj1.attributes.iteritems():
            #print "comparing attribute = " , k ,  "for objects : " , obj1.name , obj2.name
            if(k in obj1.attributes and k in obj2.attributes) :
                if obj1.attributes[k] == obj2.attributes[k]:
                    score += 1
        print "Attributes similarity score = " , score      
        return score          
          
    def getObjectMapping(self,frame1, frame2):
        obj_map =[]

        objKeys_F1 = frame1.objects.keys()
        objKeys_F2 = frame2.objects.keys()
          #to do
        if len(objKeys_F1) == len(objKeys_F2):
            print "both frames have same object count"
            obj_map.append([objKeys_F1[0] , objKeys_F2[0]])  
            score = self.compareAttributes (frame1.objects[objKeys_F1[0]] , frame2.objects[objKeys_F2[0]] )
            obj_1 = frame1.objects[objKeys_F1[0]]
            obj_2 = frame2.objects[objKeys_F2[0]]
            #score = self.compareAttributes(self,obj_1,obj_2 )
            #for attribute, value in obj_1.attributes.iteritems():
                #print "Object_1 *** : " ,obj_1.name,  attribute , value
        else:
            print " num of objects not same"
            similarity_score={}
            for key_F1 in objKeys_F1:
                for key_F2 in objKeys_F2:
                    score = self.compareAttributes(frame1.objects[key_F1] , frame2.objects[key_F2])
                    if score in similarity_score :
                        similarity_score[score].append([key_F1,key_F2])
                    else :
                        similarity_score[score] = ([key_F1,key_F2])
                        
            max_score = max(similarity_score.keys())
          
        return obj_map          

    @staticmethod
    def printDict(d):
        for k,v in d.iteritems():
            print "Key: " , k , " value = " , v


    @staticmethod
    def printFrame(frame):
        print "RPM Frame " , frame.name , "\t object_count ="  , frame.object_count
        frame.image.show()
        
