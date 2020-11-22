import numpy as np
import SimpleITK as sitk


class ItkHandler(object):

    def __init__(self):
        self.__fullImage = [[],[],[]]
    def LoadImage(self, imFile):
        try:
            self.__fullImage = self.LoadItkImage(imFile)
        except:
            print("Error in loading image\n")

    def SaveImage(self, imFile, isVector = False):
        try:
            self.SaveItkImage(imFile, self.__fullImage, isVector)
        except:
            print("Error in saving image\n")

    def GetImageVolume(self):
        return self.__fullImage[0]

    def GetImageOrigin(self):
        return self.__fullImage[1]

    def GetImageSpacing(self):
        return self.__fullImage[2]

    def GetFullImage(self):
        return self.__fullImage

    def SetImageVolumage(self, vol):
        self.__fullImage[0] = vol

    def SetImageOrigin(self, org):
        self.__fullImage[1] = org

    def SetImageSpacing(self, sp):
        self.__fullImage[2] = sp

    def SetFullImage(self, fullImage):
        self.__fullImage = fullImage

    """
     @brief: Saves an ITK image, .
     @param: fileName Name of the file to be saved.
     @param: itkImage Image to be saved. ItkImage contains image array and spatial
             coordinate details.
     @param: isVector Is the image in vector format?
     @return: NA.
     """
    @staticmethod
    def SaveItkImage(fileName, itkImage, isVector=False) :
        sitk_img = sitk.GetImageFromArray(itkImage[0], isVector)
        sitk_img.SetOrigin(np.array(list(reversed(itkImage[1]))))
        sitk_img.SetSpacing(np.array(list(reversed(itkImage[2]))))
        sitk.WriteImage(sitk_img, fileName)

    """
    @brief: Reads an image.
    @param: fileName Name of the file to be read.
    @return: ItkImage contains image array and spatial coordinate details.
    """
    @staticmethod
    def LoadItkImage(filename):
        itkimage = sitk.ReadImage(filename)
        vol = sitk.GetArrayFromImage(itkimage)
        origin = np.array(list(reversed(itkimage.GetOrigin())))
        spacing = np.array(list(reversed(itkimage.GetSpacing())))
        return vol, origin, spacing