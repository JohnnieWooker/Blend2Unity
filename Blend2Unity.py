import bpy
import random
import os
from shutil import copyfile
from shutil import rmtree
import tarfile

bl_info = {
        "name" : "Unity Tools",
        "author" : "Lukasz Hoffmann <https://www.artstation.com/artist/lukaszhoffmann>",
        "version" : (1, 0, 2),
        "blender" : (2, 7, 9),
        "location" : "View 3D > Edit Mode > Tool Shelf",
        "description" :
            "Exporting tools for Unity",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Material",
    }

def randomguid(length):
    chars=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    return ''.join(random.choice(chars) for i in range(length))

def allexport(context):
    if not os.path.exists(context.scene.my_string_prop):
        os.makedirs(context.scene.my_string_prop)
    assetname=bpy.context.selected_objects[0].name
    path=context.scene.my_string_prop+assetname+"\\"
    if not os.path.exists(path):
        os.makedirs(path)
    fbxguid=randomguid(32)
    matguid=randomguid(32)
    norguid=randomguid(32)
    metguid=randomguid(32)
    alguid=randomguid(32)
    fol1guid=randomguid(32)
    fol2guid=randomguid(32)
    #print(fbxguid)
    #export fbx
    if not os.path.exists(path+fbxguid):
        os.makedirs(path+fbxguid)
    mainexp(context, path+fbxguid+"\\asset")
    file=open(path+fbxguid+"\\asset.meta","w")
    fbxmeta="""fileFormatVersion: 2
guid: """+fbxguid+"""
timeCreated: 1505499902
licenseType: Free
ModelImporter:
  serializedVersion: 21
  fileIDToRecycleName:
    100000: //RootNode
    400000: //RootNode
    2300000: //RootNode
    3300000: //RootNode
    4300000: Armchair.001
  materials:
    importMaterials: 1
    materialName: 0
    materialSearch: 1
  animations:
    legacyGenerateAnimations: 4
    bakeSimulation: 0
    resampleCurves: 1
    optimizeGameObjects: 0
    motionNodeName: 
    rigImportErrors: 
    rigImportWarnings: 
    animationImportErrors: 
    animationImportWarnings: 
    animationRetargetingWarnings: 
    animationDoRetargetingWarnings: 0
    animationCompression: 1
    animationRotationError: 0.5
    animationPositionError: 0.5
    animationScaleError: 0.5
    animationWrapMode: 0
    extraExposedTransformPaths: []
    extraUserProperties: []
    clipAnimations: []
    isReadable: 1
  meshes:
    lODScreenPercentages: []
    globalScale: 1
    meshCompression: 0
    addColliders: 0
    importVisibility: 1
    importBlendShapes: 1
    importCameras: 1
    importLights: 1
    swapUVChannels: 0
    generateSecondaryUV: 0
    useFileUnits: 1
    optimizeMeshForGPU: 1
    keepQuads: 0
    weldVertices: 1
    secondaryUVAngleDistortion: 8
    secondaryUVAreaDistortion: 15.000001
    secondaryUVHardAngle: 88
    secondaryUVPackMargin: 4
    useFileScale: 1
  tangentSpace:
    normalSmoothAngle: 60
    normalImportMode: 0
    tangentImportMode: 3
    normalCalculationMode: 4
  importAnimation: 1
  copyAvatar: 0
  humanDescription:
    serializedVersion: 2
    human: []
    skeleton: []
    armTwist: 0.5
    foreArmTwist: 0.5
    upperLegTwist: 0.5
    legTwist: 0.5
    armStretch: 0.05
    legStretch: 0.05
    feetSpacing: 0
    rootMotionBoneName: 
    rootMotionBoneRotation: {x: 0, y: 0, z: 0, w: 1}
    hasTranslationDoF: 0
    hasExtraRoot: 0
    skeletonHasParents: 1
  lastHumanDescriptionAvatarSource: {instanceID: 0}
  animationType: 0
  humanoidOversampling: 1
  additionalBone: 0
  userData: 
  assetBundleName: 
  assetBundleVariant: """
    file.write(fbxmeta)
  
    file=open(path+fbxguid+"\\pathname","w")
    file.write("Assets/"+assetname+"/"+assetname+".fbx")


    #export normalmap
   
    normalnode=True    
    #bpy.data.objects[assetname].select = True 
    ob = bpy.data.objects[assetname]
    imagename=""
    if ob.type=='MESH':
        me=ob.data
        for slot in me.materials:
            dif=slot.node_tree.nodes['Principled BSDF']
            socket=dif.inputs[17]
            print(socket.name)
            try:
                link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                imageNode = link.from_node #The node this link is coming from
                print(imageNode.name)

                if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    image = imageNode.image #Get the image
                    imagename=image.name
                    print( "result", image.name, image.filepath )
                    newname=slot.name
                else:
                    link=next(link for link in slot.node_tree.links if link.to_node==imageNode)
                    imageNode = link.from_node #The node this link is coming from
                    print(imageNode.name)

                    if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                        image = imageNode.image #Get the image
                        imagename=image.name
                        print( "result", image.name, image.filepath )
                        newname=slot.name
                    
                                    
            except:
                print( "no link" )
                normalnode=None 
    
    print(imagename)
    if normalnode:
        if not os.path.exists(path+norguid):
            os.makedirs(path+norguid)
                  
        image = bpy.data.images[imagename]
        height=image.size[1]
        width=image.size[0]
        imgpath=bpy.path.abspath(image.filepath_raw)
        print(imgpath)
        copyfile(imgpath,path+norguid+"\\asset")    
            
        normeta="""fileFormatVersion: 2
guid: """+norguid+"""
timeCreated: 1505499899
licenseType: Free
TextureImporter:
  fileIDToRecycleName: {}
  serializedVersion: 4
  mipmaps:
    mipMapMode: 0
    enableMipMap: 1
    sRGBTexture: 0
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: """+str(height)+"""
  textureSettings:
    serializedVersion: 2
    filterMode: -1
    aniso: -1
    mipBias: -1
    wrapU: -1
    wrapV: -1
    wrapW: -1
  nPOTScale: 1
  lightmap: 0
  compressionQuality: 50
  spriteMode: 0
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spritePixelsToUnits: 100
  alphaUsage: 1
  alphaIsTransparency: 0
  spriteTessellationDetail: -1
  textureType: 1
  textureShape: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  platformSettings:
  - buildTarget: DefaultTexturePlatform
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  - buildTarget: Standalone
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
  spritePackingTag: 
  userData: 
  assetBundleName: 
  assetBundleVariant: 
    """
        file=open(path+norguid+"\\asset.meta","w")
        file.write(normeta)
        
        file=open(path+norguid+"\\pathname","w")
        file.write("Assets/"+assetname+"/"+assetname+"_Normal."+context.scene.my_enum2)
    
    
    
    
    #export metallic
    
        
       
    ob = bpy.data.objects[assetname]
    imagename=""
    metalnode=True
    if ob.type=='MESH':
        me=ob.data
        for slot in me.materials:
            dif=slot.node_tree.nodes['Principled BSDF']
            socket=dif.inputs[4]
            print(socket.name)
            try:
                link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                imageNode = link.from_node #The node this link is coming from
                print(imageNode.name)

                if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    image = imageNode.image #Get the image
                    imagename=image.name
                    print( "result", image.name, image.filepath )
                    newname=slot.name
                else:
                    link=next(link for link in slot.node_tree.links if link.to_node==imageNode)
                    imageNode = link.from_node #The node this link is coming from
                    print(imageNode.name)

                    if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                        image = imageNode.image #Get the image
                        imagename=image.name
                        print( "result", image.name, image.filepath )
                        newname=slot.name
                        
                                        
            except:
                print( "no link" )
                metalnode=None
    
    if metalnode:                
        if not os.path.exists(path+metguid):
            os.makedirs(path+metguid)                
                        
        if context.scene.my_enum=="SECOND":
            bpy.data.objects[assetname].select = True 
            bpy.context.scene.objects.active=bpy.data.objects[assetname]
            mainPBRConvert(context, path+metguid+"\\asset")                
        
        print(imagename)

                  
        image = bpy.data.images[imagename]
        height=image.size[1]
        width=image.size[0]
        imgpath=bpy.path.abspath(image.filepath_raw)
        print(imgpath)
        if context.scene.my_enum=="FIRST": 
            copyfile(imgpath,path+metguid+"\\asset")      
            
            
            
            
            
         
        metmeta="""fileFormatVersion: 2
guid: """+metguid+"""
timeCreated: 1505499900
licenseType: Free
TextureImporter:
  fileIDToRecycleName: {}
  serializedVersion: 4
  mipmaps:
    mipMapMode: 0
    enableMipMap: 1
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: """+str(height)+"""
  textureSettings:
    serializedVersion: 2
    filterMode: -1
    aniso: -1
    mipBias: -1
    wrapU: -1
    wrapV: -1
    wrapW: -1
  nPOTScale: 1
  lightmap: 0
  compressionQuality: 50
  spriteMode: 0
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spritePixelsToUnits: 100
  alphaUsage: 1
  alphaIsTransparency: 0
  spriteTessellationDetail: -1
  textureType: 0
  textureShape: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  platformSettings:
  - buildTarget: DefaultTexturePlatform
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
  spritePackingTag: 
  userData: 
  assetBundleName: 
  assetBundleVariant: 
    """   
            
        file=open(path+metguid+"\\asset.meta","w")
        file.write(metmeta)
        
        file=open(path+metguid+"\\pathname","w")
        file.write("Assets/"+assetname+"/"+assetname+"_Metallic."+context.scene.my_enum2)
    
    
    
    
    #export albedo
    
        
       
    ob = bpy.data.objects[assetname]
    imagename=""
    alnode=True
    if ob.type=='MESH':
        me=ob.data
        for slot in me.materials:
            dif=slot.node_tree.nodes['Principled BSDF']
            socket=dif.inputs[0]
            print(socket.name)
            try:
                link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                imageNode = link.from_node #The node this link is coming from
                print(imageNode.name)

                if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    image = imageNode.image #Get the image
                    imagename=image.name
                    print( "result", image.name, image.filepath )
                    newname=slot.name
                else:
                    link=next(link for link in slot.node_tree.links if link.to_node==imageNode)
                    imageNode = link.from_node #The node this link is coming from
                    print(imageNode.name)

                    if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                        image = imageNode.image #Get the image
                        imagename=image.name
                        print( "result", image.name, image.filepath )
                        newname=slot.name
                        
                                        
            except:
                print( "no link" )
                alnode=None
    if alnode:             
        if not os.path.exists(path+alguid):
            os.makedirs(path+alguid)               
        if context.scene.my_enum=="FIRST":
            bpy.data.objects[assetname].select = True 
            bpy.context.scene.objects.active=bpy.data.objects[assetname]
            mainPBRConvert(context, path+alguid+"\\asset")                
        
        print(imagename)

                  
        image = bpy.data.images[imagename]
        height=image.size[1]
        width=image.size[0]
        imgpath=bpy.path.abspath(image.filepath_raw)
        print(imgpath)
        if context.scene.my_enum=="SECOND": 
            copyfile(imgpath,path+alguid+"\\asset")
            
        almeta="""fileFormatVersion: 2
guid: """+alguid+"""
timeCreated: 1505499902
licenseType: Free
TextureImporter:
  fileIDToRecycleName: {}
  serializedVersion: 4
  mipmaps:
    mipMapMode: 0
    enableMipMap: 1
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
  isReadable: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: """+str(height)+"""
  textureSettings:
    serializedVersion: 2
    filterMode: -1
    aniso: -1
    mipBias: -1
    wrapU: -1
    wrapV: -1
    wrapW: -1
  nPOTScale: 1
  lightmap: 0
  compressionQuality: 50
  spriteMode: 0
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spritePixelsToUnits: 100
  alphaUsage: 1
  alphaIsTransparency: 0
  spriteTessellationDetail: -1
  textureType: 0
  textureShape: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  platformSettings:
  - buildTarget: DefaultTexturePlatform
    maxTextureSize: """+str(height)+"""
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
  spritePackingTag: 
  userData: 
  assetBundleName: 
  assetBundleVariant: 
     
    """        
        
        file=open(path+alguid+"\\asset.meta","w")
        file.write(almeta)
        
        file=open(path+alguid+"\\pathname","w")
        file.write("Assets/"+assetname+"/"+assetname+"_Albedo."+context.scene.my_enum2)                  

    #export material
    if not os.path.exists(path+matguid):
        os.makedirs(path+matguid)
    file=open(path+matguid+"\\pathname","w")
    file.write("Assets/"+assetname+"/Materials/Material.mat")     
        
    matmeta="""fileFormatVersion: 2
guid: """+matguid+"""
timeCreated: 1505559282
licenseType: Free
NativeFormatImporter:
  mainObjectFileID: 2100000
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""    

    file=open(path+matguid+"\\asset.meta","w")
    file.write(matmeta)
    
    sm=1
    
    
    smoothness=""
    if context.scene.my_enum=="FIRST":
        smoothness="""SMOOTHNESS_TEXTURE_METALLIC_CHANNEL_A _METALLICGLOSSMAP _NORMALMAP
    _SMOOTHNESS_TEXTURE_ALBEDO_CHANNEL_A"""
    if context.scene.my_enum=="SECOND":
        sm=0
        smoothness="""SMOOTHNESS_TEXTURE_METALLIC_CHANNEL_A _METALLICGLOSSMAP _NORMALMAP"""    
    
    normalstr="{x: 1, y: 1}"
    metalstr="{x: 1, y: 1}"
    alstr="{x: 1, y: 1}"
    
    if normalnode:
        normalstr="{fileID: 2800000, guid: "+norguid+", type: 3}"
    if metalnode:
        metalstr="{fileID: 2800000, guid: "+metguid+", type: 3}"
    if alnode:
        alstr="{fileID: 2800000, guid: "+alguid+", type: 3}"    
    
    matasset="""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!21 &2100000
Material:
  serializedVersion: 6
  m_ObjectHideFlags: 0
  m_PrefabParentObject: {fileID: 0}
  m_PrefabInternal: {fileID: 0}
  m_Name: Material
  m_Shader: {fileID: 46, guid: 0000000000000000f000000000000000, type: 0}
  m_ShaderKeywords: """+smoothness+"""
  m_LightmapFlags: 4
  m_EnableInstancingVariants: 0
  m_DoubleSidedGI: 0
  m_CustomRenderQueue: -1
  stringTagMap: {}
  disabledShaderPasses: []
  m_SavedProperties:
    serializedVersion: 3
    m_TexEnvs:
    - _BumpMap:
        m_Texture: """+normalstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _DetailAlbedoMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _DetailMask:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _DetailNormalMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _EmissionMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _MainTex:
        m_Texture: """+alstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _MetallicGlossMap:
        m_Texture: """+metalstr+"""
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _OcclusionMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    - _ParallaxMap:
        m_Texture: {fileID: 0}
        m_Scale: {x: 1, y: 1}
        m_Offset: {x: 0, y: 0}
    m_Floats:
    - _BumpScale: 1
    - _Cutoff: 0.5
    - _DetailNormalMapScale: 1
    - _DstBlend: 0
    - _GlossMapScale: 1
    - _Glossiness: 0.5
    - _GlossyReflections: 1
    - _Metallic: 0
    - _Mode: 0
    - _OcclusionStrength: 1
    - _Parallax: 0.02
    - _SmoothnessTextureChannel: """+str(sm)+"""
    - _SpecularHighlights: 1
    - _SrcBlend: 1
    - _UVSec: 0
    - _ZWrite: 1
    m_Colors:
    - _Color: {r: 1, g: 1, b: 1, a: 1}
    - _EmissionColor: {r: 0, g: 0, b: 0, a: 1}
"""
    
    file=open(path+matguid+"\\asset","w")
    file.write(matasset)
    
    #folder1
    
    if not os.path.exists(path+fol1guid):
        os.makedirs(path+fol1guid)
    file=open(path+fol1guid+"\\pathname","w")
    file.write("Assets/"+assetname)  
    
    fol1asset="""fileFormatVersion: 2
guid: """+fol1guid+"""
folderAsset: yes
timeCreated: 1505557484
licenseType: Free
DefaultImporter:
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""
    file=open(path+fol1guid+"\\asset.meta","w")
    file.write(fol1asset)
    
     #folder2
    
    if not os.path.exists(path+fol2guid):
        os.makedirs(path+fol2guid)
    file=open(path+fol2guid+"\\pathname","w")
    file.write("Assets/"+assetname+"/Materials")  
    
    fol2asset="""fileFormatVersion: 2
guid: """+fol2guid+"""
folderAsset: yes
timeCreated: 1505557484
licenseType: Free
DefaultImporter:
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""
    file=open(path+fol2guid+"\\asset.meta","w")
    file.write(fol2asset)
    file.close()
    
    output=context.scene.my_string_prop+assetname+".unitypackage"
    dir=path     
    make_tarfile(output, dir)       
    
    rmtree(path)

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:bz2") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def checknode(index):
    ob = bpy.context.object
    if ob.type=='MESH':
        me=ob.data
        mat_offset=len(me.materials)
        for slot in me.materials:
            
            dif = slot.node_tree.nodes['Principled BSDF']
            socket2=dif.inputs[index]
    

def mainPBRConvert(context, path):
    mapsonly=None
    if not os.path.exists(context.scene.my_string_prop):
        os.makedirs(context.scene.my_string_prop)
    
    if path=="thisisnotunityexport":
        mapsonly=True
        
        
    if mapsonly:    
        print("maps only")
    else:
        print("unitypackage export")    
    path=path
    mapnames=['Albedo','Subsurface','Subsurface_Radius','Subsurface_Color','Metallic','Specular','Speular_Tint','Rooughness','Anisotropic','Anisotropic_Rotation','Sheen','Sheen_Tint','Clearcoat','Clearcoat_Roughness','IOR','Transmission','Unknown','Normal','Clearcoat_Normal','Tangent']
        
    mapstoexpo=[]
    
    if context.scene.my_enum=="SECOND" and context.scene.my_boolal:
        mapstoexpo.append(0)
    if context.scene.my_enum=="FIRST" and context.scene.my_boolme:
        mapstoexpo.append(4)
    if context.scene.my_boolno:
        mapstoexpo.append(17)
    
    roughnode=True
    resultname=""
    newname=""
    imagename=""
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)
    ob = bpy.context.object
    if ob.type=='MESH':
        me=ob.data
        mat_offset=len(me.materials)
        for slot in me.materials:
            
            dif = slot.node_tree.nodes['Principled BSDF']
            socket2=dif.inputs[7]
            
            nodes=0
            
            if context.scene.my_enum=="FIRST" and context.scene.my_boolal:
                socket = dif.inputs[0]
                print("Converting Roughness to Albedo alpha")
                resultname="Albedo"
            if context.scene.my_enum=="SECOND" and context.scene.my_boolme:
                socket=dif.inputs[4]
                print("Converting Roughness to Metallic alpha")
                resultname="Metallic"        
            try:
                link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                imageNode = link.from_node #The node this link is coming from

                if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    image = imageNode.image #Get the image
                    imagename=image.name
                    print( "result", image.name, image.filepath )
                    newname=slot.name                
            except:
                print( "no link" )
                nodes=nodes+1            
            try:
                link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket2)
                imageNode = link.from_node #The node this link is coming from

                if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node

                    image = imageNode.image #Get the image
                    roughimagename=image.name
                    print( "result", roughimagename, image.filepath )                 
            except:
                print( "no link" )
                nodes=nodes+1
                roughnode=None
    if nodes<2:
        if roughnode:                    
            imageold = bpy.data.images[imagename]  
            alpha=bpy.data.images[roughimagename]
            width = imageold.size[0]
            height = imageold.size[1]
            bpy.ops.image.new(name="PBR_Diff", width=width, height=height)
            image = bpy.data.images['PBR_Diff']  
            index=0
            Alpha_list=list(alpha.pixels)
            Alpha_list_new=[]
            RGBA_list = list(imageold.pixels)
            RGBA_list_new=[]
            for i in RGBA_list:    
                RGBA_list_new.append(i)
            index=0    
            for i in RGBA_list_new:
                if index%4==0:
                    r=abs(Alpha_list[index]-1)
                    g=abs(Alpha_list[index+1]-1)
                    b=abs(Alpha_list[index+2]-1)
                    al=mean([r,g,b])
                    RGBA_list_new[index+3]=al
                    #print(str(RGBA_list_new[index+3]))
                index=index+1
            image.pixels=RGBA_list_new
            
            filetp=""
            if context.scene.my_enum2=="PNG":
                filetp='png'
            else:
                filetp='tga'
            if mapsonly:
                path=context.scene.my_string_prop+newname+"_"+resultname+"."+filetp    
            image.filepath_raw = path
            image.file_format = context.scene.my_enum2            
            image.save()
            image.user_clear()
            bpy.data.images.remove(image)
            
        
        else:
            imageold = bpy.data.images[imagename]
            width = imageold.size[0]
            height = imageold.size[1]
            bpy.ops.image.new(name="PBR_Diff", width=width, height=height)
            RGBA_list = list(imageold.pixels)            
            image = bpy.data.images['PBR_Diff']
            image.pixels=RGBA_list
            filetp=""
            if context.scene.my_enum2=="PNG":
                filetp='png'
            else:
                filetp='tga'
            if mapsonly:
                path=context.scene.my_string_prop+newname+"_"+resultname+"."+filetp    
            image.filepath_raw = path
            image.file_format = context.scene.my_enum2
            image.save()
            image.user_clear()
            bpy.data.images.remove(image)            
            
    ob = bpy.context.object
    if ob.type=='MESH':
        me=ob.data
        mat_offset=len(me.materials)
        for slot in me.materials: 
                      
            olddif = slot.node_tree.nodes['Principled BSDF']        
            dif = slot.node_tree.nodes['Principled BSDF']        
            for m in mapstoexpo:
                istex=None
                print("Exporting: "+str(m))
                socket=dif.inputs[m]
                for i in range (0,10):
                    try:
                        if i>0 and not imageNode.name==olddif.name:                            
                            link=next(link for link in slot.node_tree.links if link.to_node==dif)
                        else:    
                            link=next(link for link in slot.node_tree.links if link.to_node==dif and link.to_socket == socket)
                        imageNode = link.from_node #The node this link is coming from

                        if imageNode.type == 'TEX_IMAGE': #Check if it is an image texture node
                            print(imageNode.name)
                            image = imageNode.image #Get the image
                            imagename=image.name
                            print( "result", image.name, image.filepath )
                            newname=slot.name
                            istex=True
                            break 
                        else:
                            print(imageNode.name)
                            dif=imageNode
                                       
                    except:
                        print( "no link" )
                        break
                if istex:
                    imageold = bpy.data.images[imagename]
                    width = imageold.size[0]
                    height = imageold.size[1]
                    bpy.ops.image.new(name="Temporary_map_to_export", width=width, height=height)
                    RGBA_list = list(imageold.pixels)            
                    image = bpy.data.images['Temporary_map_to_export']
                    image.pixels=RGBA_list
                    filetp=""
                    if context.scene.my_enum2=="PNG":
                        filetp='png'
                    else:
                        filetp='tga'
                       
                    if mapsonly:
                        path=context.scene.my_string_prop+newname+"_"+mapnames[m]+"."+filetp
                        print("Exporting "+mapnames[m])
                        image.filepath_raw = path
                        image.file_format = context.scene.my_enum2
                        image.save()
                        image.user_clear()
                        bpy.data.images.remove(image)                         

def mainmatuni(context):
    scene = bpy.context.scene

    def isclose(a, b, rel_tol=1e-09, abs_tol=context.scene.my_string_prop2):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def replace_material(object,old_material,new_material):
        """
        replace a material in blender.
        params:
            object - object for which we are replacing the material
            old_material - The old material name as a string
            new_material - The new material name as a string
        """
        ob = object
        om = bpy.data.materials[old_material]
        nm = bpy.data.materials[new_material]
        # Iterate over the material slots and replace the material
        for s in ob.material_slots:
            if s.material.name == old_material:
                s.material = nm

    materialsmerged=0

    selected = bpy.context.selected_objects

    for obj in selected:
        #print(obj.name)
        if obj.type=='MESH':
            for slot in obj.data.materials:
                color_base=slot.diffuse_color
                for obj_match in selected:
                    if obj_match.type=='MESH':
                        for slot_match in obj_match.data.materials:
                            color_match=slot_match.diffuse_color
                            if isclose(color_base[0],color_match[0]):
                                if isclose(color_base[1],color_match[1]):
                                    if isclose(color_base[2],color_match[2]):
                                        if slot!=slot_match:
                                            print("match "+slot.name+" i simmilar to "+slot_match.name)
                                            replace_material(obj,slot.name,slot_match.name)
                                            materialsmerged+=1                                       

                                        
    print("merged "+str(materialsmerged)+" materials")

def mainexp(context, name):
    if not os.path.exists(context.scene.my_string_prop):
        os.makedirs(context.scene.my_string_prop)    
    selected = bpy.context.selected_objects
    lst = []
    for obj in selected:
        lst.append(obj.name)
        me = obj.data
        me.use_auto_smooth=True
        me.auto_smooth_angle=180
        me.name=obj.name

    if context.scene.my_bool:
        for str in lst:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[str].select = True            
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            
            if context.scene.my_bool2:
                
                bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
                
                obj  = bpy.context.selected_objects[0]
                mesh = obj.data
                lowestv=mesh.vertices[0].co[2]
                #print(lowestv)
            
                for v in mesh.vertices:
                    #print(v.co[2])
                    if v.co[2]<lowestv:
                        lowestv=v.co[2]
                    
                print(lowestv)
            
                for v in mesh.vertices:
                    v.co[2]-=lowestv
            
            if name=="thisisnotunitypackage":
                bpy.ops.export_scene.fbx(filepath=context.scene.my_string_prop+str+".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, bake_space_transform=True, global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
            else:
                bpy.ops.export_scene.fbx(filepath=name, check_existing=True, filter_glob="*.fbx", use_selection=True, bake_space_transform=True, global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
            bpy.ops.object.delete(use_global=False)
    else:
        #str=bpy.context.selected_objects[0].name
        lst2=[]
        for str in lst:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[str].select = True
            
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            if context.scene.my_bool2:
                bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
                
                obj  = bpy.context.selected_objects[0]
                lst2.append(obj.name)
                mesh = obj.data
                lowestv=mesh.vertices[0].co[2]
                #print(lowestv)
            
                for v in mesh.vertices:
                    #print(v.co[2])
                    if v.co[2]<lowestv:
                        lowestv=v.co[2]
                    
                print(lowestv)
            
                for v in mesh.vertices:
                    v.co[2]-=lowestv
                
        for str in lst2:
            #print(str)        
            bpy.data.objects[str].select = True    
        
        nm=bpy.path.basename(bpy.context.blend_data.filepath)
        nm=nm[:nm.index(".blend")]
        print(nm)        
        bpy.ops.export_scene.fbx(filepath=context.scene.my_string_prop+nm+".fbx", check_existing=True, filter_glob="*.fbx", use_selection=True, bake_space_transform=True, global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=False, mesh_smooth_type='EDGE', use_mesh_edges=False, use_armature_deform_only=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
        bpy.ops.object.delete(use_global=False)

def mainconv(context):
    selected = bpy.context.selected_objects
    lst = []
    for obj in selected:
        lst.append(obj.name)
        me = obj.data
        me.use_auto_smooth=True
        me.auto_smooth_angle=180
        me.name=obj.name
    
    for str in lst:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[str].select = True  
        ob = bpy.context.object
        if ob.type=='MESH':
            me = ob.data
            mat_offset = len(me.materials)
            for slot in me.materials:
                slot.specular_intensity=0.05
                slot.diffuse_intensity=1
                slot.specular_hardness=10
                slot.use_nodes=False
                slot.diffuse_color=slot.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value[0],slot.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value[1],slot.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value[2]

def maintrans(context):
    selected = bpy.context.selected_objects
    lst = []

    for obj in selected:
        lst.append(obj.name)
        me = obj.data    
        me.name=obj.name
        
        
    for str in lst:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[str].select = True
        bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
        obj  = bpy.data.objects[str]
        mesh = obj.data
        lowestv=mesh.vertices[0].co[2]
        #print(lowestv)
        
        for v in mesh.vertices:
            #print(v.co[2])
            if v.co[2]<lowestv:
                lowestv=v.co[2]
                
        print(lowestv)
        
        for v in mesh.vertices:
            v.co[2]-=lowestv
    
class UnityTransform(bpy.types.Operator):
    """Correct object transformation. Apply location, rotation, scale an center pivot on lowest vertex"""
    bl_idname="cusops.unitytransform"
    bl_label="Correct transform"
    
    def execute(self,context):
        maintrans(context)
        return{'FINISHED'}
    
class UnityMatConv(bpy.types.Operator):
    """Convert Cycles materials to Internal materials (required when using the same materials in Unity)"""
    bl_idname="cusops.unitymatconv"
    bl_label="Convert materials"
    
    def execute(self,context):
        mainconv(context)
        return{'FINISHED'}
    
class UnityExport(bpy.types.Operator):
    """Export selected objects to FBX file/files"""
    bl_idname="cusops.unityexport"
    bl_label="Export to FBX"
    
    def execute(self,context):
        mainexp(context, "thisisnotunitypackage")
        return{'FINISHED'}
    
class AllExport(bpy.types.Operator):
    """Export as unitypackage"""
    bl_idname="cusops.allexport"
    bl_label="Export unitypackage"
    
    def execute(self,context):
        allexport(context)
        return{'FINISHED'}

class PBRConvert(bpy.types.Operator):
    """Convert PBR Roughness to Unity PBR Albedo_Smoothness. Required texture inputs in Roughness and Base Color or Metallic channels of Principled BSDF node"""
    bl_idname="cusops.pbrconvert"
    bl_label="Export texture set"
    
    def execute(self,context):
        mainPBRConvert(context, "thisisnotunityexport")
        return{'FINISHED'}               
    
class UnityMatMerge(bpy.types.Operator):
    """Merge similar materials. Use threshold to control similarity comparision"""
    bl_idname="cusops.unitymatmerge"
    bl_label="Unify materials"
    
    def execute(self,context):
        mainmatuni(context)
        return{'FINISHED'}            


    
class OpenBrowser(bpy.types.Operator):
        bl_idname = "open.browser"
        bl_label = "Choose export directory"

        filepath = bpy.props.StringProperty(subtype="FILE_PATH") 
        #somewhere to remember the address of the file


        def execute(self, context):
            folpath=self.filepath
            index=folpath.rfind('\\')
            folpath=folpath[:index]
            display = "filepath= "+folpath
            print(display) #Prints to console  
            context.scene.my_string_prop=folpath+"\\"
            #Window>>>Toggle systen console

            return {'FINISHED'}

        def invoke(self, context, event): # See comments at end  [1]

            context.window_manager.fileselect_add(self) 
            #Open browser, take reference to 'self' 
            #read the path to selected file, 
            #put path in declared string type data structure self.filepath

            return {'RUNNING_MODAL'}
        
class OpenBrowser2(bpy.types.Operator):
        bl_idname = "open.browser2"
        bl_label = "Choose directory"

        filepath = bpy.props.StringProperty(subtype="FILE_PATH") 
        #somewhere to remember the address of the file


        def execute(self, context):
            folpath=self.filepath
            index=folpath.rfind('\\')
            folpath=folpath[:index]
            display = "filepath= "+folpath
            print(display) #Prints to console  
            context.scene.my_string_prop3=folpath+"\\"
            #Window>>>Toggle systen console

            return {'FINISHED'}

        def invoke(self, context, event): # See comments at end  [1]

            context.window_manager.fileselect_add(self) 
            #Open browser, take reference to 'self' 
            #read the path to selected file, 
            #put path in declared string type data structure self.filepath

            return {'RUNNING_MODAL'}                
    
def register():
    bpy.utils.register_class(AllExport)
    bpy.utils.register_class(PBRConvert)
    bpy.utils.register_class(OpenBrowser)
    bpy.utils.register_class(OpenBrowser2)
    bpy.utils.register_class(UnityTransform)
    bpy.utils.register_class(UnityMatConv)
    bpy.utils.register_class(UnityExport)
    bpy.utils.register_class(UnityMatMerge)
    bpy.types.Scene.my_string_prop = bpy.props.StringProperty \
    (
     name = "Path",
     description = "Path to export",
     default = "D:\\Export\\"
    )
    bpy.types.Scene.my_string_prop2 = bpy.props.FloatProperty \
    (
     name = "Threshold",
     description = "Marging threshold",
     default = 0.1
    )
    bpy.types.Scene.my_string_prop3 = bpy.props.StringProperty \
    (
     name = "Path",
     description = "Choose where to save your texture",
     default = "D:\\Export\\"
    )
    bpy.types.Scene.my_bool = bpy.props.BoolProperty(
    name="Separate files",
    description="Choose whehter to export objects in separate fbx file or in one",
    default = True) 
    bpy.types.Scene.my_bool2 = bpy.props.BoolProperty(
    name="Auto transform correction",
    description="Automatically correct transform while exporting",
    default = True)
    bpy.types.Scene.my_boolal = bpy.props.BoolProperty(
    name="Albedo",
    description="Check to export Albedo map",
    default = True) 
    bpy.types.Scene.my_boolme = bpy.props.BoolProperty(
    name="Metallic",
    description="Check to export Metallic Map",
    default = True)
    bpy.types.Scene.my_boolro = bpy.props.BoolProperty(
    name="Roughness",
    description="Check to export Roughness Map",
    default = True)  
    bpy.types.Scene.my_boolno = bpy.props.BoolProperty(
    name="Normal Map",
    description="Check to export Normal Map",
    default = True)  
    bpy.types.Scene.my_enum = bpy.props.EnumProperty(
        name = "Smoothness",
        description = "Choose whether to save smoothness alpha channel on albedo or metallic",
        items = [
            ("FIRST" , "Albedo Alpha" , "Cast roughness as alpha to albedo map"),
            ("SECOND", "Metallic Alpha", "Cast roughness as alpha to metallic map")
        ]
    )
    bpy.types.Scene.my_enum2 = bpy.props.EnumProperty(
        name = "Filetype",
        description = "Choose type of image",
        items = [
            ("PNG" , "PNG" , "Cast roughness as alpha to albedo map"),
            ("TARGA", "TGA", "Cast roughness as alpha to metallic map")
        ]
    )
    
def unregister():
    bpy.utils.unregister_class(AllExport)
    bpy.utils.unregister_class(PBRConvert)
    bpy.utils.unregister_class(OpenBrowser)
    bpy.utils.unregister_class(OpenBrowser2)
    bpy.utils.unregister_class(UnityTransform)
    bpy.utils.unregister_class(UnityMatConv)
    bpy.utils.unregister_class(UnityExport)
    bpy.utils.unregister_class(UnityMatMerge)
    del bpy.types.Scene.my_string_prop
    del bpy.types.Scene.my_bool
    del bpy.types.Scene.my_string_prop2
    del bpy.types.Scene.my_string_prop3
    del bpy.types.Scene.my_bool2
    del bpy.types.Scene.my_enum
    del bpy.types.Scene.my_enum2

register()

#bpy.ops.UnityTransform






















class UnityExporterPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Unity Exporter"
    bl_idname = "OBJECT_PT_UExporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Unity Export Tools"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        #row = layout.row()
        #row.label(text="Material tools")

        #row = layout.row()
        #row.operator("cusops.unitytransform")
        
        #row = layout.row()
        #row.operator("cusops.unitymatconv")
        
        #row = layout.row()
        #row.operator("cusops.unitymatmerge")
        
        #row = layout.row()
        #row.prop(context.scene, "my_string_prop2")
        
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        #row.label(text="FBX Export")
        
        
		
        row = layout.row()
        row.prop(context.scene, "my_string_prop")
        row.operator("open.browser", icon="FILE_FOLDER", text="")
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator("cusops.unityexport")
        
        row = layout.row()
        row.prop(context.scene, "my_bool")

        row = layout.row()
        row.prop(context.scene, "my_bool2")
        
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.label(text="Unity PBR textures")
        row = layout.row()
        row.prop(context.scene, "my_boolal")
        row = layout.row()
        row.prop(context.scene, "my_boolme")
        row = layout.row()
        row.prop(context.scene, "my_boolno")
        
        row = layout.row()
        row.label(text="Roughness>Smoothness")
        
        
        
        #row = layout.row()
        #row.prop(context.scene, "my_string_prop3")
        #row.operator("open.browser2", icon="FILE_FOLDER", text="")
        
        row = layout.row()
        row.prop(context.scene, "my_enum")
        
        row = layout.row()
        row.prop(context.scene, "my_enum2")
        
        row = layout.row()
        row.operator("cusops.pbrconvert")
        
        row = layout.row()
        row.operator("cusops.allexport")

def register():
    bpy.utils.register_class(UnityExporterPanel)


def unregister():
    bpy.utils.unregister_class(UnityExporterPanel)


if __name__ == "__main__":
    register()

