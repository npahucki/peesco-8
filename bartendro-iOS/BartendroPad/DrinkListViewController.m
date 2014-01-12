//
//  ViewController.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/3/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkListViewController.h"

@interface DrinkListViewController () < UITextFieldDelegate,
                                        UICollectionViewDataSource,
                                        UICollectionViewDelegateFlowLayout>

@property (strong, nonatomic) NSMutableArray * topDrinkList;
@property (strong, nonatomic) NSMutableArray * otherDrinkList;

@property (strong, nonatomic) IBOutlet UICollectionView * DrinksMenu;

@end

@implementation DrinkListViewController

- (void)viewDidLoad
{
  
  
    [super viewDidLoad];
    
    [self getDrinkList];

}



-(void) getDrinkList{
  
    NSString * getAddress = [NSString stringWithFormat:@"http://%@/ws/drink/dindex", BARTENDRO_URL];
  
    AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];
    
    [manager GET:getAddress
      parameters:nil
     
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             NSLog(@"JSON: %@", responseObject);
             
             NSArray * td = [[[responseObject objectForKey:@"AllDrinks"] objectAtIndex:0] objectForKey:@"topDrinks"];
             NSArray * od = [[[responseObject objectForKey:@"AllDrinks"] objectAtIndex:1] objectForKey:@"otherDrinks"];
           NSMutableArray * allDrinks = [[NSMutableArray alloc] initWithArray:td];
           [allDrinks addObjectsFromArray:od];
           
             //             NSLog(@"top drinks  : %@", td);
             //             NSLog(@"Other drinks  : %@", td);
           
             [self fillTopDrinkListFromJSON:allDrinks];
//             [self fillOtherDrinkListFromJSON:od];
           
             
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];



}


- (void) fillTopDrinkListFromJSON:(NSArray *) jsonList{

    self.topDrinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.topDrinkList addObject:d];
    }
    
    NSLog(@"We have %d Top drinks", [self.topDrinkList count]);
    [self.DrinksMenu reloadData];
    
}


- (void) fillOtherDrinkListFromJSON:(NSArray *) jsonList{
    
    
    self.otherDrinkList = [[NSMutableArray alloc] init];
    
    for (NSDictionary * dict in jsonList){
        
        //NSLog(@"dict: %@", dict);
        
        Drink * d = [[Drink alloc] init];
        [d fillWithAttributes:dict];
        [self.otherDrinkList addObject:d];
    }
    
    NSLog(@"We have %d other drinks", [self.otherDrinkList count]);
    [self.DrinksMenu reloadData];
    
}


- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - UICollectionView Datasource

- (NSInteger)collectionView:(UICollectionView *)view numberOfItemsInSection:(NSInteger)section {

    
//    NSLog(@"Section: %d", section);
//    NSLog(@"topDrinkList: %d", [self.topDrinkList count]);
////    NSLog(@"otherDrinkList: %d", [self.otherDrinkList count]);
//  
//    NSInteger retvalue = 0;
//    
//    switch (section) {
//        case 0:
//            
//           retvalue = [self.topDrinkList count];
//            
//            break;
//        case 1:
//            retvalue = [self.otherDrinkList count];
//            break;
//            
//        default:
//            retvalue = 0;
//            break;
//    }
//    
//    NSLog(@"Drinks %d para la section %d", retvalue, section);
  
    
//    return retvalue;
  
  return [self.topDrinkList count];
}

- (NSInteger)numberOfSectionsInCollectionView: (UICollectionView *)collectionView {
//    return [self.searches count];
    return 1;
}

- (UICollectionViewCell *)collectionView:(UICollectionView *)cv
                  cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    
    DrinkCollectionViewCell * cell = [cv dequeueReusableCellWithReuseIdentifier:@"DrinkCell"
                                                                   forIndexPath:indexPath];
    
    Drink * d;
    
    NSLog(@"La row: %d", indexPath.row);
    NSLog(@"La seccion: %d", indexPath.section);
    
//    switch (indexPath.section) {
//        case 0:
//            d = [self.topDrinkList objectAtIndex:indexPath.row];
//            break;
//            
//        case 1:
//            d = [self.otherDrinkList objectAtIndex:indexPath.row];
//            break;
//            
//        default:
//            break;
//    }
    d = [self.topDrinkList objectAtIndex:indexPath.row];
  
    [cell populateUIwithDatafrom:d];
    cell.serveDrinkDelegate=self;
   
    return cell;
}


//- (UICollectionReusableView *)collectionView:
// (UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
// {
// return [[UICollectionReusableView alloc] init];
//}

-(void) serveDrinkWithId:(int)drinkId
{
  MBProgressHUD *hud = [[MBProgressHUD alloc] initWithView:self.view.window];
  hud.mode = MBProgressHUDModeText;
  hud.labelText = @"Sirviendo...";
  hud.labelFont = [UIFont fontWithName:@"DIN Alternate" size:30];
  hud.margin = 50.f;
  hud.minSize = CGSizeMake(200.f, 200.f);
  hud.color = [self colorWithHexString:@"f2804a"];
  hud.removeFromSuperViewOnHide = YES;
  [self.view.window addSubview:hud];
  [hud show:YES];

  NSString * get = [NSString stringWithFormat:@"http://%@/ws/drink/%d",BARTENDRO_URL,  drinkId];
  NSLog(@"Calling : %@", get);
  
  AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];
  
  [manager GET:get
    parameters:nil
   
   
       success:^(AFHTTPRequestOperation *operation, id responseObject) {
         NSLog(@"JSON: %@", responseObject);
         [hud hide:YES];
       }
   
       failure:^(AFHTTPRequestOperation *operation, NSError *error) {
         NSLog(@"Error trying to serve drink: %@", error);
         [hud hide:YES];
       }
   ];
 
}

- (UICollectionReusableView *)collectionView:(UICollectionView *)collectionView viewForSupplementaryElementOfKind:(NSString *)kind atIndexPath:(NSIndexPath *)indexPath
{
    UICollectionReusableView *reusableview = nil;
    
    if (kind == UICollectionElementKindSectionHeader) {
        
        HeaderCollectionReusableView *headerView =
      [collectionView dequeueReusableSupplementaryViewOfKind:UICollectionElementKindSectionHeader
                                         withReuseIdentifier:@"HeaderView"
                                                forIndexPath:indexPath];
        
//        NSString *title;
//        
//        
//        if (indexPath.section == 0) {
//                title = [[NSString alloc] initWithFormat:@"Lo tipico"];
//        }
//        
//        if (indexPath.section == 1) {
//            title = [[NSString alloc] initWithFormat:@"Lo Esencial"];
//        }
//        
////        headerView.tituloHeader.text = title;
      
//      [1/11/14, 11:07:25 PM] Simon Forgacs: 0e1e6
//      [1/11/14, 11:08:24 PM] Simon Forgacs: Color of the button background e0e1e6
//      [1/11/14, 11:08:35 PM] Simon Forgacs: f2804a
      
//
//        headerView.backgroundColor = [self colorWithHexString:@"00e1e6"];
        reusableview = headerView;
    }
    
    
    return reusableview;
}

#pragma mark - UICollectionViewDelegate

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    // TODO: Select Item
}

- (void)collectionView:(UICollectionView *)collectionView didDeselectItemAtIndexPath:(NSIndexPath *)indexPath {
    // TODO: Deselect item
}


-(UIColor*)colorWithHexString:(NSString*)hex
{
  NSString *cString = [[hex stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] uppercaseString];
  
  // String should be 6 or 8 characters
  if ([cString length] < 6) return [UIColor grayColor];
  
  // strip 0X if it appears
  if ([cString hasPrefix:@"0X"]) cString = [cString substringFromIndex:2];
  
  if ([cString length] != 6) return  [UIColor grayColor];
  
  // Separate into r, g, b substrings
  NSRange range;
  range.location = 0;
  range.length = 2;
  NSString *rString = [cString substringWithRange:range];
  
  range.location = 2;
  NSString *gString = [cString substringWithRange:range];
  
  range.location = 4;
  NSString *bString = [cString substringWithRange:range];
  
  // Scan values
  unsigned int r, g, b;
  [[NSScanner scannerWithString:rString] scanHexInt:&r];
  [[NSScanner scannerWithString:gString] scanHexInt:&g];
  [[NSScanner scannerWithString:bString] scanHexInt:&b];
  
  return [UIColor colorWithRed:((float) r / 255.0f)
                         green:((float) g / 255.0f)
                          blue:((float) b / 255.0f)
                         alpha:1.0f];
}













@end
