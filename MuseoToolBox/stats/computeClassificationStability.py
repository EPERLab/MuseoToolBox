# coding: utf-8
from .. import rasterTools
import os
from scipy import stats
import numpy as np
import sys

class modalClass():
    def __init__(
            self,
            inRaster,
            outRaster,
            inMaskRaster,
            outGdalDT,
            outNoData):
        #process = rasterTools.readAndWriteRaster(inRaster,outRaster=outRaster,inMaskRaster=inMaskRaster,outNBand=2,outGdalGDT=outGdalDT,outNoData=outNoData)
        
        process = rasterTools.rasterMath(inRaster, inMaskRaster)
        process.addFunction(self.stabCalc, outRaster, 2, 3, outNoData)
        process.run()

    def stabCalc(self, arr):
        tmp = stats.mode(arr, axis=-1)
        tmpStack = np.column_stack((tmp[0], tmp[1]))
        return tmpStack



def modalClassCLI(argv=None, apply_config=True):
    import argparse
    if len(sys.argv) == 1:
        prog = os.path.basename(sys.argv[0])
        print(sys.argv[0] + ' [options]')
        print("Help : ", prog, " --help")
        print("or : ", prog, " -h")
        print(
            2 *
            ' ' +
            "example 1 : ",
            prog,
            " -in raster.tif -out modal.tif")
        sys.exit(-1)

    else:
        usage = "usage: %prog [options] "
        parser = argparse.ArgumentParser(
            description="Compute modal class (first band) and number of agreements (second band).",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument(
            "-in",
            "--image",
            dest="inRaster",
            action="store",
            help="Image to extract values from and to generate centroid from output vector",
            required=True)

        parser.add_argument(
            "-inm",
            "--inMaskRaster",
            dest="inMaskRaster",
            action="store",
            help="Vector to fill with raster values",
            required=False,
            default=False,
            type=str)

        parser.add_argument(
            "-out",
            "--outRaster",
            dest="outRaster",
            action="store",
            help="Raster to save (geotif)",
            required=True,
            type=str)
        args = parser.parse_args()
    
        modalClass(
                inRaster=args.inRaster,
                outRaster=args.outRaster,
                inMaskRaster=args.inMaskRaster,
                outGdalDT=3,
                outNoData=0)


if __name__ == "__main__":
    sys.exit(modalClassCLI())



